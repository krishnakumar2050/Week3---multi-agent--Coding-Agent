# Code review report

Status: **complete**

Static test-gap analysis only; tests were not executed and coverage was not measured.

critical: 0 | high: 7 | medium: 13 | low: 0 | info: 0

Run: `1b686ab7-1910-43ce-be92-d593db92e733` · Schema: 1.0

Repository: `/Users/krishnakumar/Documents/github/Omni-Notes`

Snapshot SHA-256: `41fc505a0701571ccae3fa4445a7a1287879f582163ce88921f074202dc6f16e`

Completed: 2026-10-25T06:24:28.910874+00:00 · Duration: 50.903 seconds

## Model provenance

| Agent | Requested model | Actual model | Evidence |
| --- | --- | --- | --- |
| quality | CLI default | gpt-6.1-sol | codex_cli_startup |
| security | CLI default | gpt-6.1-sol | codex_cli_startup |
| tests | CLI default | gpt-6.1-sol | codex_cli_startup |

## Agent 1 anti-pattern knowledge

Keenable status: ok

- Java Code Review Checklist: Best Practices and Common Pitfalls — https://pullpanda.io/blog/java-code-review-checklist
- claude-code-java/.claude/skills/java-code-review/SKILL.md at main · decebals/claude-code-java — https://github.com/decebals/claude-code-java/blob/main/.claude/skills/java-code-review/SKILL.md
- Java Code Review Checklist | Engineering Guidelines — https://guidelines.ryanharrison.co.uk/languages/java/java-code-review
- code-review-skill/reference/java8.md at 4850184dfd7765ea7b3c5c4e9b6cf8e0815ee7cb · awesome-skills/code-review-skill — https://github.com/awesome-skills/code-review-skill/blob/HEAD/reference/java8.md
- software-engineering-skills/plugins/java/skills/java-code-review/SKILL.md at main · wesleyegberto/software-engineering-skills — https://github.com/wesleyegberto/software-engineering-skills/blob/main/plugins/java/skills/java-code-review/SKILL.md
- code-review-best-practices/example-guidelines/languages/java.yaml at main · augmentcode/code-review-best-practices — https://github.com/augmentcode/code-review-best-practices/blob/main/example-guidelines/languages/java.yaml

External guidance supplements source analysis; it is not repository evidence.

## 1. [HIGH] Note updates leave transactions open when an operation throws

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:266` · Agents: quality

The transaction begun at line 227 has no finally cleanup. An exception during attachment processing, such as dereferencing a null attachment URI at line 309, skips endTransaction(), retaining the transaction and potentially blocking subsequent database operations.

Fix: Wrap the transaction body in try/finally, mark success only after all writes succeed, and always call endTransaction() in finally.

Suggested test: Force an attachment write to throw; assert the note update rolls back and another thread can subsequently write to the database.

Evidence:

````
    db.setTransactionSuccessful();
    db.endTransaction();
````

## 2. [HIGH] Migration errors are swallowed before destructive statements continue

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:283` · Agents: quality

This is the swallowed-exception anti-pattern. In upgrade-501.sql, if copying notes fails because two existing notes share a creation timestamp, execution still reaches DROP TABLE notes_tmp. The upgrade can then complete and commit after deleting the original notes.

Fix: Propagate SQL failures so SQLiteOpenHelper rolls back the upgrade transaction and preserves the original database.

Suggested test: Upgrade a database containing duplicate creation timestamps; assert the upgrade fails and all original notes remain available.

Evidence:

````
      try {
        db.execSQL(sqlInstruction);
      } catch (Exception e) {
        LogDelegate.e("Error executing command: " + sqlInstruction, e);
      }
````

## 3. [HIGH] SQL migration failures are swallowed before destructive statements

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:283` · Agents: tests

Execution continues after a failed migration statement. In upgrade-501.sql, a failed INSERT into the replacement notes table is followed by DROP TABLE notes_tmp. For example, duplicate creation timestamps cause the new primary key insertion to fail, after which the original notes are dropped and the upgrade can report success.

Fix: Propagate SQL failures so SQLiteOpenHelper rolls back the upgrade. Define how duplicate creation timestamps are migrated before enforcing uniqueness.

Suggested test: Create a pre-501 database containing two notes with distinct note_id values and identical creation timestamps. Upgrade it and assert that either both notes and their attachments survive with valid identifiers, or the upgrade fails and the original schema and records remain intact.

Evidence:

````
      try {
        db.execSQL(sqlInstruction);
      } catch (Exception e) {
        LogDelegate.e("Error executing command: " + sqlInstruction, e);
      }
````

## 4. [HIGH] Millisecond attachment IDs can overwrite other attachments

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:306` · Agents: quality

Two new attachments saved in the same millisecond receive the same primary key. The CONFLICT_REPLACE insertion at line 314 then deletes the earlier attachment row. The generated ID is also never assigned back to the attachment, so saving the same new object again can insert another row.

Fix: Let SQLite generate IDs for new attachments, capture the inserted row ID, and assign it to the attachment. Preserve explicit IDs only for existing rows.

Suggested test: Save multiple attachments with a fixed clock, then save them again; assert every attachment has a distinct persisted ID and the row count remains unchanged on the second save.

Evidence:

````
    valuesAttachments.put(KEY_ATTACHMENT_ID,
        attachment.getId() != null ? attachment.getId() : Calendar.getInstance().getTimeInMillis());
````

## 5. [HIGH] Stored password verifier also serves as the note decryption key

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:473` · Agents: security

PasswordHelper verifies passwords against the MD5 value in PREF_PASSWORD, but this stored value is also passed directly to encryption and decryption. An attacker obtaining the preferences and database can decrypt locked notes without recovering the password. Security additionally uses DES, which limits effective key strength to 56 bits.

Fix: Use authenticated encryption with a key protected by Android Keystore or derived from the entered password using a salted password KDF. Keep the authentication verifier separate and migrate existing ciphertext.

Suggested test: Verify that copying the database and password-verifier preferences does not provide sufficient material to decrypt a locked note.

Evidence:

````
          // Eventual decryption of content
          if (Boolean.TRUE.equals(note.isLocked())) {
            note.setContent(
                Security.decrypt(note.getContent(), Prefs.getString(PREF_PASSWORD, "")));
          }
````

## 6. [HIGH] Encryption failure silently persists plaintext

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66` · Agents: quality

This is fail-open exception handling. For example, a password shorter than eight UTF-8 bytes makes DESKeySpec fail, and encrypt returns the original content. DbHelper.updateNote then persists that plaintext while retaining the locked flag, presenting the note as protected.

Fix: Propagate encryption failure and abort the save; never substitute plaintext for failed encryption.

Suggested test: Attempt to save a locked note with an invalid encryption key; assert the save reports failure and no plaintext is written.

Evidence:

````
            } catch (e: Exception) {
                LogDelegate.e("Something is gone wrong encrypting", e)
                value
            }
````

## 7. [HIGH] Encryption failures silently persist plaintext as locked content

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66` · Agents: tests

An encryption error returns the original plaintext. DbHelper.updateNote stores that return value while retaining the locked flag. A password shorter than eight UTF-8 bytes triggers DESKeySpec failure, including the empty default preference value. The supplied encryption test exercises only a valid long password and misses this failure path.

Fix: Fail explicitly when encryption fails and prevent the database write from proceeding with plaintext.

Suggested test: Call encrypt with an empty password and a seven-byte password and assert explicit failure. Attempt to save a locked note with the password preference absent and assert that plaintext is never persisted and any previous record remains unchanged.

Evidence:

````
            } catch (e: Exception) {
                LogDelegate.e("Something is gone wrong encrypting", e)
                value
            }
````

## 8. [MEDIUM] Gallery initialization indexes an explicitly permitted empty list

Location: `omniNotes/src/main/java/it/feio/android/omninotes/GalleryActivity.java:163` · Agents: tests

initData defaults missing GALLERY_IMAGES to Collections.emptyList(), then unconditionally indexes it here. Missing or empty images therefore crash initialization. Negative or out-of-range GALLERY_CLICKED_IMAGE values also crash, even if ViewPager clamps its own current item.

Fix: Handle empty images before configuring the gallery and validate the requested index before accessing the list.

Suggested test: Launch GalleryActivity with missing images, an empty image list, and a single image with indices -1 and 1. Assert graceful completion or a defined fallback without IndexOutOfBoundsException.

Evidence:

````
    if (images.get(clickedImage).getMime_type().equals(MIME_TYPE_VIDEO)) {
      viewMedia();
    }
````

## 9. [MEDIUM] Opening media crashes when no viewer is installed

Location: `omniNotes/src/main/java/it/feio/android/omninotes/GalleryActivity.java:190` · Agents: quality

A device without an activity supporting the attachment's MIME type throws ActivityNotFoundException. Videos invoke this path automatically during gallery initialization, so simply opening such a video crashes the gallery.

Fix: Catch ActivityNotFoundException and display a clear message while keeping the gallery usable.

Suggested test: Open a video with no matching external viewer installed; assert the gallery remains open and reports that no viewer is available.

Evidence:

````
      Intent intent = new Intent(Intent.ACTION_VIEW);
      intent.setFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
      intent.setDataAndType(shareableAttachmentUri, getMimeType(this, attachment.getUri()));
      startActivity(intent);
````

## 10. [MEDIUM] Activity weak reference is dereferenced before the lifecycle guard

Location: `omniNotes/src/main/java/it/feio/android/omninotes/async/MainMenuTask.java:61` · Agents: quality

If the activity is destroyed and collected while the background task runs, mainActivity.get() returns null and onPostExecute crashes before reaching isAlive().

Fix: Resolve weak references once into local variables, validate the activity and fragment lifecycle first, and only then access the drawer.

Suggested test: Destroy the hosting activity before task completion and clear its weak reference; assert completion exits without accessing views or throwing.

Evidence:

````
    navDrawer = mainActivity.get().findViewById(R.id.drawer_nav_list);
    if (isAlive()) {
````

## 11. [MEDIUM] Main menu completion dereferences the activity before checking its lifecycle

Location: `omniNotes/src/main/java/it/feio/android/omninotes/async/MainMenuTask.java:61` · Agents: tests

The activity is held only through a WeakReference and can be collected while the task runs. onPostExecute dereferences it before the lifecycle guard, causing a NullPointerException instead of discarding the result.

Fix: Capture strong local references, validate both the activity and fragment lifecycle, and only then look up and update the drawer.

Suggested test: Delay menu construction, detach and destroy the host, and simulate a cleared activity reference before completion. Assert completion performs no view updates and throws no exception.

Evidence:

````
    navDrawer = mainActivity.get().findViewById(R.id.drawer_nav_list);
    if (isAlive()) {
````

## 12. [MEDIUM] Today's reminders are selected using UTC dates

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:653` · Agents: quality

SQLite evaluates both dates in UTC. In a non-UTC timezone, reminders near midnight can fall on a different local day, so getTodayReminders omits reminders due today and includes reminders due yesterday or tomorrow.

Fix: Compute the local day's start and next day's start in the application timezone and query the timestamp interval.

Suggested test: In Australia/Melbourne, query reminders around local midnight and assert only timestamps within the current local calendar day are returned.

Evidence:

````
        " WHERE DATE(" + KEY_REMINDER + "/1000, 'unixepoch') = DATE('now') AND " +
            KEY_TRASHED + " IS NOT 1";
````

## 13. [MEDIUM] Tag search interpolates input into executable SQL

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:763` · Agents: security

Tag values are inserted into SQL string literals without escaping or binding, and getNotes executes the resulting query with rawQuery. If an attacker can influence a searched tag, an apostrophe can cause an uncaught SQL error, while crafted SQL can alter the selection. The later regex filter runs only after SQL execution and cannot prevent injection.

Fix: Bind tag patterns through selection arguments, escaping LIKE metacharacters when literal matching is intended.

Suggested test: Search for tags containing apostrophes and SQL syntax; assert that they are treated literally, do not throw, and do not broaden the SQL selection.

Evidence:

````
      whereCondition.append(String.format("((%s IS 1 AND %s LIKE '%%%s%%') OR (%s is NOT 1 AND (%s LIKE '%%%s%%' OR %s LIKE '%%%s%%')))"
          , KEY_LOCKED, KEY_TITLE, tags[i], KEY_LOCKED, KEY_CONTENT, tags[i], KEY_TITLE, tags[i]));
````

## 14. [MEDIUM] Tag searches interpolate unescaped text into SQL

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:763` · Agents: tests

A tag containing an apostrophe breaks the SQL literal and can cause query failure. Tags are also inserted directly into Pattern.compile at line 774, so regex metacharacters can change matching or throw PatternSyntaxException. The supplied tag navigation test uses only #hashtag and does not assert search results.

Fix: Bind SQL arguments, escape LIKE metacharacters for literal matching, and quote tag text with Pattern.quote before building the regex.

Suggested test: Seed notes with literal tags containing an apostrophe and regex metacharacters, then call getNotesByTag with those values. Assert no exception and that only notes containing the exact requested tag are returned; include an empty tag array with explicitly defined behavior.

Evidence:

````
      whereCondition.append(String.format("((%s IS 1 AND %s LIKE '%%%s%%') OR (%s is NOT 1 AND (%s LIKE '%%%s%%' OR %s LIKE '%%%s%%')))"
          , KEY_LOCKED, KEY_TITLE, tags[i], KEY_LOCKED, KEY_CONTENT, tags[i], KEY_TITLE, tags[i]));
````

## 15. [MEDIUM] Tag values are interpolated directly into SQL

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:763` · Agents: quality

A tag argument containing an apostrophe produces malformed SQL and an uncaught database exception. Unlike getNotesByPattern, this method does not escape its input. SQL metacharacters can also change the query's meaning.

Fix: Pass tag patterns as bound selection arguments, escaping LIKE wildcards when literal matching is intended.

Suggested test: Search for a tag containing an apostrophe; assert the query completes and returns only literal matches.

Evidence:

````
      whereCondition.append(String.format("((%s IS 1 AND %s LIKE '%%%s%%') OR (%s is NOT 1 AND (%s LIKE '%%%s%%' OR %s LIKE '%%%s%%')))"
          , KEY_LOCKED, KEY_TITLE, tags[i], KEY_LOCKED, KEY_CONTENT, tags[i], KEY_TITLE, tags[i]));
````

## 16. [MEDIUM] Notification cancellation does not match the identity used by show

Location: `omniNotes/src/main/java/it/feio/android/omninotes/helpers/notifications/NotificationsHelper.java:207` · Agents: tests

show(long) posts notifications with a string tag and numeric ID 0, but cancel(int) and cancel() use the untagged cancellation overload. Consequently, show(42) followed by cancel(42), or show() followed by cancel(), leaves the posted notification active.

Fix: Use consistent tag and ID pairs for posting and cancellation, while preserving the separate untagged progress notification behavior if needed.

Suggested test: Post with show(42), cancel that notification, and assert its tagged entry is absent from active notifications. Repeat with show() and cancel(), and verify cancellation leaves an unrelated notification intact.

Evidence:

````
    mNotificationManager.notify(String.valueOf(id), 0, mBuilder.build());
````

## 17. [MEDIUM] Notification cancellation uses a different identity from posting

Location: `omniNotes/src/main/java/it/feio/android/omninotes/helpers/notifications/NotificationsHelper.java:207` · Agents: quality

show(long) posts notifications with a string tag and integer ID 0, but cancel(int) calls cancel(id), which addresses an untagged notification. Thus show(42) followed by cancel(42) leaves the notification visible. updateMessage(int) and finish(int) likewise post under a different identity.

Fix: Use one consistent tag/ID convention across posting, updating, finishing, and cancellation.

Suggested test: Post with show(42), update it, and cancel it; assert there is exactly one notification after updating and none after cancellation.

Evidence:

````
    mNotificationManager.notify(String.valueOf(id), 0, mBuilder.build());
````

## 18. [MEDIUM] Encryption failures silently persist plaintext

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66` · Agents: security

Any encryption exception returns the original note content. DbHelper.updateNote stores that result while retaining the locked flag. For example, the empty default PREF_PASSWORD produces an invalid DES key, so saving a locked note in that state stores plaintext that an attacker with database access can read.

Fix: Propagate encryption failures and abort the database update. Never return plaintext as a successful encryption result.

Suggested test: Attempt to save a locked note with missing key material; assert that saving fails and no plaintext is written.

Evidence:

````
            } catch (e: Exception) {
                LogDelegate.e("Something is gone wrong encrypting", e)
                value
            }
````

## 19. [MEDIUM] Widget display preferences are shared globally and lost on restart

Location: `omniNotes/src/main/java/it/feio/android/omninotes/widget/ListRemoteViewsFactory.java:65` · Agents: quality

This is hidden shared mutable state: thumbnail and timestamp settings are static fields used by every widget, while only the SQL condition is persisted per widget. Configuring a second widget changes the first widget's display, and process restart resets both settings to true.

Fix: Persist both display settings under widget-specific keys and load them into instance fields for each factory.

Suggested test: Configure two widgets with opposite display settings, recreate their factories, and assert each retains its own settings.

Evidence:

````
  static void updateConfiguration(int mAppWidgetId, String sqlCondition, boolean thumbnails, boolean timestamps) {
    LogDelegate.d("Widget configuration updated");
    Prefs.edit().putString(PREF_WIDGET_PREFIX + mAppWidgetId, sqlCondition).apply();
    showThumbnails = thumbnails;
    showTimestamps = timestamps;
  }
````

## 20. [MEDIUM] Widget fill-in intents expose decrypted locked notes to the host

Location: `omniNotes/src/main/java/it/feio/android/omninotes/widget/ListRemoteViewsFactory.java:127` · Agents: security

DbHelper.getNotes decrypts locked content before returning notes. This code embeds the entire note in RemoteViews delivered to the widget host, and Note.writeToParcel includes its content. If a locked note is included in the widget query, a malicious widget host can inspect its plaintext even when the displayed text is masked.

Fix: Put only the note identifier in widget fill-in intents. Retrieve the note inside the app and require authentication before exposing locked content.

Suggested test: Include a locked note in a widget and inspect the delivered RemoteViews intent extras; assert that neither plaintext content nor the full Note parcel is present.

Evidence:

````
    Bundle extras = new Bundle();
    extras.putParcelable(INTENT_NOTE, note);
    Intent fillInIntent = new Intent();
    fillInIntent.putExtras(extras);
    // Make it possible to distinguish the individual on-click
    // action of a given item
    row.setOnClickFillInIntent(R.id.root, fillInIntent);
````

## Review limitations

- quality: ok
  - Review was limited to the supplied snapshot; no tools or execution were used.
  - Caller validation, dependency implementations, build configuration, and manifest overlays were not supplied, so their effects could not be verified.
- security: ok
  - Reviewed only the supplied snapshot without execution.
  - External reachability of tag-search input cannot be confirmed because MainActivity and its routing implementation are absent.
  - Widget configuration, preference initialization, backup behavior, and the merged manifest are not fully supplied.
- tests: ok
  - Static review only; no tools were called and no tests were executed.
  - Only the supplied snapshot was reviewed. Omitted callers, base test classes, dependencies, and build configuration may affect reachability and test setup.
  - Missing tests described here refer only to the supplied tests, not the complete repository suite.
