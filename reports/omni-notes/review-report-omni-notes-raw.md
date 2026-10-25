# Code review report

Status: **complete**

Static batched analysis only. Gradle builds, Android tests, runtime coverage, and exploit reproduction were not performed. Cross-batch relationships may be missed.

critical: 0 | high: 19 | medium: 72 | low: 4 | info: 0

## Model provenance

| Agent | Requested model | Actual model | Evidence |
| --- | --- | --- | --- |
| quality | CLI default | gpt-6.1-sol | codex_cli_startup |
| security | CLI default | gpt-6.1-sol | codex_cli_startup |
| tests | CLI default | gpt-6.1-sol | codex_cli_startup |
| quality | CLI default | gpt-6.1-sol | codex_cli_startup |
| security | CLI default | gpt-6.1-sol | codex_cli_startup |
| tests | CLI default | gpt-6.1-sol | codex_cli_startup |
| quality | CLI default | gpt-6.1-sol | codex_cli_startup |
| security | CLI default | gpt-6.1-sol | codex_cli_startup |
| tests | CLI default | gpt-6.1-sol | codex_cli_startup |
| quality | CLI default | gpt-6.1-sol | codex_cli_startup |
| security | CLI default | gpt-6.1-sol | codex_cli_startup |
| tests | CLI default | gpt-6.1-sol | codex_cli_startup |
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

## Agent 1 anti-pattern knowledge

Keenable status: ok

- Java Code Review Checklist: Best Practices and Common Pitfalls — https://pullpanda.io/blog/java-code-review-checklist
- claude-code-java/.claude/skills/java-code-review/SKILL.md at main · decebals/claude-code-java — https://github.com/decebals/claude-code-java/blob/main/.claude/skills/java-code-review/SKILL.md
- Java Code Review Checklist | Engineering Guidelines — https://guidelines.ryanharrison.co.uk/languages/java/java-code-review
- code-review-skill/reference/java8.md at 4850184dfd7765ea7b3c5c4e9b6cf8e0815ee7cb · awesome-skills/code-review-skill — https://github.com/awesome-skills/code-review-skill/blob/HEAD/reference/java8.md
- software-engineering-skills/plugins/java/skills/java-code-review/SKILL.md at main · wesleyegberto/software-engineering-skills — https://github.com/wesleyegberto/software-engineering-skills/blob/main/plugins/java/skills/java-code-review/SKILL.md
- code-review-best-practices/example-guidelines/languages/java.yaml at main · augmentcode/code-review-best-practices — https://github.com/augmentcode/code-review-best-practices/blob/main/example-guidelines/languages/java.yaml

External guidance supplements source analysis; it is not repository evidence.

## Agent 1 anti-pattern knowledge

Keenable status: ok

- Java Code Review Checklist: Best Practices and Common Pitfalls — https://pullpanda.io/blog/java-code-review-checklist
- claude-code-java/.claude/skills/java-code-review/SKILL.md at main · decebals/claude-code-java — https://github.com/decebals/claude-code-java/blob/main/.claude/skills/java-code-review/SKILL.md
- Java Code Review Checklist | Engineering Guidelines — https://guidelines.ryanharrison.co.uk/languages/java/java-code-review
- code-review-skill/reference/java8.md at 4850184dfd7765ea7b3c5c4e9b6cf8e0815ee7cb · awesome-skills/code-review-skill — https://github.com/awesome-skills/code-review-skill/blob/HEAD/reference/java8.md
- software-engineering-skills/plugins/java/skills/java-code-review/SKILL.md at main · wesleyegberto/software-engineering-skills — https://github.com/wesleyegberto/software-engineering-skills/blob/main/plugins/java/skills/java-code-review/SKILL.md
- code-review-best-practices/example-guidelines/languages/java.yaml at main · augmentcode/code-review-best-practices — https://github.com/augmentcode/code-review-best-practices/blob/main/example-guidelines/languages/java.yaml

External guidance supplements source analysis; it is not repository evidence.

## Agent 1 anti-pattern knowledge

Keenable status: ok

- Java Code Review Checklist: Best Practices and Common Pitfalls — https://pullpanda.io/blog/java-code-review-checklist
- claude-code-java/.claude/skills/java-code-review/SKILL.md at main · decebals/claude-code-java — https://github.com/decebals/claude-code-java/blob/main/.claude/skills/java-code-review/SKILL.md
- Java Code Review Checklist | Engineering Guidelines — https://guidelines.ryanharrison.co.uk/languages/java/java-code-review
- code-review-skill/reference/java8.md at 4850184dfd7765ea7b3c5c4e9b6cf8e0815ee7cb · awesome-skills/code-review-skill — https://github.com/awesome-skills/code-review-skill/blob/HEAD/reference/java8.md
- software-engineering-skills/plugins/java/skills/java-code-review/SKILL.md at main · wesleyegberto/software-engineering-skills — https://github.com/wesleyegberto/software-engineering-skills/blob/main/plugins/java/skills/java-code-review/SKILL.md
- code-review-best-practices/example-guidelines/languages/java.yaml at main · augmentcode/code-review-best-practices — https://github.com/augmentcode/code-review-best-practices/blob/main/example-guidelines/languages/java.yaml

External guidance supplements source analysis; it is not repository evidence.

## Agent 1 anti-pattern knowledge

Keenable status: ok

- Java Code Review Checklist: Best Practices and Common Pitfalls — https://pullpanda.io/blog/java-code-review-checklist
- claude-code-java/.claude/skills/java-code-review/SKILL.md at main · decebals/claude-code-java — https://github.com/decebals/claude-code-java/blob/main/.claude/skills/java-code-review/SKILL.md
- Java Code Review Checklist | Engineering Guidelines — https://guidelines.ryanharrison.co.uk/languages/java/java-code-review
- code-review-skill/reference/java8.md at 4850184dfd7765ea7b3c5c4e9b6cf8e0815ee7cb · awesome-skills/code-review-skill — https://github.com/awesome-skills/code-review-skill/blob/HEAD/reference/java8.md
- software-engineering-skills/plugins/java/skills/java-code-review/SKILL.md at main · wesleyegberto/software-engineering-skills — https://github.com/wesleyegberto/software-engineering-skills/blob/main/plugins/java/skills/java-code-review/SKILL.md
- code-review-best-practices/example-guidelines/languages/java.yaml at main · augmentcode/code-review-best-practices — https://github.com/augmentcode/code-review-best-practices/blob/main/example-guidelines/languages/java.yaml

External guidance supplements source analysis; it is not repository evidence.

## 1. [HIGH] Application password protection can be disabled without authentication

Location: `omniNotes/src/main/java/it/feio/android/omninotes/SettingsFragment.java:335` · Agents: security

Returning true accepts and persists the switch change immediately, independently of the password callback. Someone with access to an open application session can disable application password protection and cancel or fail the password prompt; the unsuccessful callback does not restore the setting.

Fix: Return false and change the persisted switch state only after successful password validation.

Suggested test: With application password protection enabled, toggle it off and cancel or fail authentication. Assert that the switch and persisted preference remain enabled after reopening settings.

Evidence:

````
      passwordAccess.setOnPreferenceChangeListener((preference, newValue) -> {
        PasswordHelper.requestPassword(getActivity(), passwordConfirmed -> {
          if (passwordConfirmed.equals(Result.SUCCEED)) {
            passwordAccess.setChecked((Boolean) newValue);
          }
        });
        return true;
      });
````

## 2. [HIGH] Password access can be disabled without successful authentication

Location: `omniNotes/src/main/java/it/feio/android/omninotes/SettingsFragment.java:335` · Agents: quality

Returning true allows SwitchPreference to immediately persist the requested value while password validation is pending. A user can disable password access and cancel or fail the password prompt; no failure branch restores the original value.

Fix: Return false from the change listener and update the checked state only after successful password validation.

Suggested test: Enable password access, request disabling it, then cancel or enter an incorrect password. Assert that both the switch and persisted preference remain enabled.

Evidence:

````
      passwordAccess.setOnPreferenceChangeListener((preference, newValue) -> {
        PasswordHelper.requestPassword(getActivity(), passwordConfirmed -> {
          if (passwordConfirmed.equals(Result.SUCCEED)) {
            passwordAccess.setChecked((Boolean) newValue);
          }
        });
        return true;
      });
````

## 3. [HIGH] Password access changes persist before authentication succeeds

Location: `omniNotes/src/main/java/it/feio/android/omninotes/SettingsFragment.java:335` · Agents: tests

Returning true lets SwitchPreference immediately accept and persist the requested value. Failed or cancelled authentication does not undo that change, so disabling password access does not require successful password validation.

Fix: Return false and apply the new checked value only in the successful authentication callback.

Suggested test: Start with a configured password and password access enabled. Toggle access off, then submit an incorrect password or cancel. Assert the switch and persisted preference remain enabled. Repeat with the correct password and assert both become disabled.

Evidence:

````
      passwordAccess.setOnPreferenceChangeListener((preference, newValue) -> {
        PasswordHelper.requestPassword(getActivity(), passwordConfirmed -> {
          if (passwordConfirmed.equals(Result.SUCCEED)) {
            passwordAccess.setChecked((Boolean) newValue);
          }
        });
        return true;
      });
````

## 4. [HIGH] Duplicate-creation migration can preserve duplicates and update multiple notes

Location: `omniNotes/src/main/java/it/feio/android/omninotes/async/upgrade/UpgradeProcessor.java:171` · Agents: quality

Two notes sharing creation, title, and content both match this UPDATE and receive the same new creation value, so they remain duplicates. Even for distinct content, the random offset can be zero or collide with another creation. This fails the migration's uniqueness requirement before creation becomes the primary key, potentially preventing the transition.

Fix: Update each row by its existing unique ID and allocate a deterministic unused creation value, tracking newly assigned values.

Suggested test: Migrate two identical notes with the same creation plus nearby occupied timestamps; assert that every row survives and all resulting creation values are unique.

Evidence:

````
        ContentValues values = new ContentValues();
        values.put(DbHelper.KEY_CREATION, note.getCreation() + (long) (Math.random() * 999));
        DbHelper.getInstance().getDatabase()
            .update(DbHelper.TABLE_NOTES, values, DbHelper.KEY_TITLE +
                    " = ? AND " + DbHelper.KEY_CREATION + " = ? AND " + DbHelper.KEY_CONTENT + " = ?",
                new String[]{note
                    .getTitle(), String.valueOf(note.getCreation()), note.getContent()});
````

## 5. [HIGH] Note updates leave transactions open when an operation throws

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:266` · Agents: quality

The transaction begun at line 227 has no finally cleanup. An exception during attachment processing, such as dereferencing a null attachment URI at line 309, skips endTransaction(), retaining the transaction and potentially blocking subsequent database operations.

Fix: Wrap the transaction body in try/finally, mark success only after all writes succeed, and always call endTransaction() in finally.

Suggested test: Force an attachment write to throw; assert the note update rolls back and another thread can subsequently write to the database.

Evidence:

````
    db.setTransactionSuccessful();
    db.endTransaction();
````

## 6. [HIGH] Migration errors are swallowed before destructive statements continue

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

## 7. [HIGH] SQL migration failures are swallowed before destructive statements

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

## 8. [HIGH] Millisecond attachment IDs can overwrite other attachments

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:306` · Agents: quality

Two new attachments saved in the same millisecond receive the same primary key. The CONFLICT_REPLACE insertion at line 314 then deletes the earlier attachment row. The generated ID is also never assigned back to the attachment, so saving the same new object again can insert another row.

Fix: Let SQLite generate IDs for new attachments, capture the inserted row ID, and assign it to the attachment. Preserve explicit IDs only for existing rows.

Suggested test: Save multiple attachments with a fixed clock, then save them again; assert every attachment has a distinct persisted ID and the row count remains unchanged on the second save.

Evidence:

````
    valuesAttachments.put(KEY_ATTACHMENT_ID,
        attachment.getId() != null ? attachment.getId() : Calendar.getInstance().getTimeInMillis());
````

## 9. [HIGH] Stored password verifier also serves as the note decryption key

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

## 10. [HIGH] Persistable folder permission flags always evaluate to zero

Location: `omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:273` · Agents: quality

Read and write permission flags are distinct bits, so their bitwise AND is zero. The selected backup folder therefore receives no persisted read or write grant, leaving later backup operations without access once the temporary grant expires.

Fix: Mask intent.getFlags() with the bitwise OR of the read and write flags, and persist the granted permissions.

Suggested test: Select a backup folder, restart the device, and assert that its persisted URI permission includes read and write access and a backup can complete.

Evidence:

````
    final int takeFlags = FLAG_GRANT_READ_URI_PERMISSION & FLAG_GRANT_WRITE_URI_PERMISSION;
    context.getContentResolver().takePersistableUriPermission(intent.getData(), takeFlags);
````

## 11. [HIGH] Note parceling loses the database ID

Location: `omniNotes/src/main/java/it/feio/android/omninotes/models/Note.java:169` · Agents: quality

Neither writeToParcel nor the parcel constructor preserves the note ID. Existing notes passed through an Intent or restored fragment arguments therefore lose their database identity. SnoozeActivity subsequently saves such notes or forwards note.get_id(), potentially updating the wrong identity or creating a duplicate.

Fix: Write the note ID into the parcel and read it back in the matching position.

Suggested test: Round-trip a persisted note through Parcel and assert that its ID and all other persisted fields remain equal.

Evidence:

````
  public void writeToParcel(Parcel parcel, int flags) {
    parcel.writeString(String.valueOf(getCreation()));
    parcel.writeString(String.valueOf(getLastModification()));
````

## 12. [HIGH] Backup encryption truncates the password hash to a weak DES key

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:58` · Agents: security

BackupHelper.exportNote passes PREF_PASSWORD into this function, and PasswordActivity stores that value as hexadecimal MD5. DESKeySpec uses only the first eight bytes, so the encryption key has at most 32 bits of input entropy from eight hexadecimal characters, further reduced by DES parity bits. An attacker who obtains a locked-note backup can brute-force this small key space offline regardless of the original password's strength.

Fix: Use authenticated encryption such as AES-GCM with a random nonce and a properly salted password derivation function. Version the backup format and retain legacy decryption only for migration.

Suggested test: Verify that two password inputs sharing their first eight characters cannot decrypt each other's new-format ciphertext, repeated encryption produces different ciphertext, and modified ciphertext is rejected.

Evidence:

````
                val keySpec = DESKeySpec(password.toByteArray(StandardCharsets.UTF_8))
                val keyFactory = SecretKeyFactory.getInstance("DES")
                val key = keyFactory.generateSecret(keySpec)
                val clearText = value.toByteArray(StandardCharsets.UTF_8)
                // Cipher is not thread safe
                val cipher = Cipher.getInstance("DES")
````

## 13. [HIGH] Note encryption uses a truncated DES key

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:58` · Agents: security

An attacker who obtains encrypted notes can attack them offline. DES uses only the first eight password bytes and has at most 56 effective key bits. The password flow demonstrated in BackupHelperTest passes hexadecimal MD5 text, limiting those eight bytes to at most 32 bits of entropy before DES parity removal. Longer passwords therefore do not provide corresponding encryption strength.

Fix: Use a salted password KDF with an appropriate work factor and authenticated encryption such as AES-GCM. Version the encrypted format and migrate existing DES ciphertext after successful authentication.

Suggested test: Verify that passwords sharing their first eight bytes produce independently decryptable ciphertext only with their respective full passwords, and that modified ciphertext fails authentication.

Evidence:

````
                val keySpec = DESKeySpec(password.toByteArray(StandardCharsets.UTF_8))
                val keyFactory = SecretKeyFactory.getInstance("DES")
                val key = keyFactory.generateSecret(keySpec)
                val clearText = value.toByteArray(StandardCharsets.UTF_8)
                // Cipher is not thread safe
                val cipher = Cipher.getInstance("DES")
````

## 14. [HIGH] Cryptographic failures silently return unprocessed content

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66` · Agents: quality

This is fail-open exception handling. Encryption failure returns plaintext as though encryption succeeded, allowing exportNote to write unencrypted content for a locked note. The corresponding decrypt catch also returns its input, so a backup encrypted with another password can be persisted by importNote as ciphertext instead of being rejected.

Fix: Return an explicit cryptographic failure or throw a dedicated exception from both operations. Abort the affected export or import before writing content when encryption or decryption fails.

Suggested test: Force encryption failure and assert that no plaintext backup is written. Import a locked backup with an incorrect password and assert that no note is persisted.

Evidence:

````
            } catch (e: Exception) {
                LogDelegate.e("Something is gone wrong encrypting", e)
                value
            }
````

## 15. [HIGH] Encryption failure silently persists plaintext

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

## 16. [HIGH] Encryption failure silently returns plaintext

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66` · Agents: tests

Encryption errors are reported as successful string results containing the original secret. For example, a password shorter than eight UTF-8 bytes cannot construct the DES key and takes this path. Callers cannot distinguish ciphertext from unencrypted content.

Fix: Return an explicit failure or throw an exception, and ensure callers do not persist the input when encryption fails.

Suggested test: Call encrypt with value "private note" and password "short". Assert an explicit encryption failure and verify that the plaintext is never returned as an encrypted result or persisted.

Evidence:

````
            } catch (e: Exception) {
                LogDelegate.e("Something is gone wrong encrypting", e)
                value
            }
````

## 17. [HIGH] Encryption failures return plaintext as a successful result

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66` · Agents: quality, security

This is a fail-open exception-handling anti-pattern. For example, a password shorter than eight bytes causes DESKeySpec construction to fail, after which encrypt returns the original sensitive value. Callers cannot distinguish plaintext from successful encryption and may store or transmit it.

Fix: Propagate an explicit encryption failure and prevent persistence or transmission until encryption succeeds. Never return the input as an encryption fallback.

Suggested test: Encrypt a sensitive value with a password shorter than eight bytes; assert an explicit failure and that no plaintext result is returned.
Encrypt a sensitive value with a password shorter than eight UTF-8 bytes and assert that the operation reports failure and never returns the input value.

Evidence:

````
            } catch (e: Exception) {
                LogDelegate.e("Something is gone wrong encrypting", e)
                value
            }
````

## 18. [HIGH] Encryption failures return plaintext as successful output

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66` · Agents: quality

This is fail-open exception handling. A password shorter than eight UTF-8 bytes causes DESKeySpec construction to fail, and encrypt returns the original sensitive value. Callers cannot distinguish this from successful encryption and may store or export plaintext.

Fix: Propagate a specific encryption failure or return an explicit failure result; never return plaintext on encryption failure.

Suggested test: Encrypt sensitive text with a short password and assert an explicit failure with no plaintext returned.

Evidence:

````
            } catch (e: Exception) {
                LogDelegate.e("Something is gone wrong encrypting", e)
                value
            }
````

## 19. [HIGH] Encryption failures silently persist plaintext as locked content

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

## 20. [MEDIUM] Upgrade assertion also passes if migration deletes attachments

Location: `omniNotes/src/androidTest/java/it/feio/android/omninotes/async/upgrade/UpgradeProcessorTest.kt:41` · Agents: tests

allMatch returns true for an empty collection. The test therefore accepts loss of every attachment, and it does not establish that the migrated URI still points to the original data needed for backups.

Fix: Assert preservation of the note and attachment identities and count, then read the migrated attachment and compare its contents.

Suggested test: Seed one content URI attachment with known bytes, migrate, reload its note, and assert exactly one attachment remains with the original identity, a usable file URI, and identical bytes.

Evidence:

````
        UpgradeProcessor.process(624, 625)

        assertTrue(dbHelper.allAttachments.stream().allMatch { a -> a.uri.scheme != "content" });
````

## 21. [MEDIUM] Retry loop exits before the timeout

Location: `omniNotes/src/androidTest/java/it/feio/android/omninotes/testutils/RetryableAssert.java:54` · Agents: tests

The loop repeats only when the clock exactly equals the deadline. For a normal positive timeout it exits immediately, so asynchronous assertions fail before their allowed waiting period.

Fix: Retry while the deadline has not passed, return on success, and fail only after the timeout.

Suggested test: Use a predicate that becomes true after 100 ms with a 1000 ms timeout and assert success. Also verify that an always-false predicate fails after the allowed interval.

Evidence:

````
    while (System.currentTimeMillis() == endTime);
````

## 22. [MEDIUM] RetryableAssert does not wait for its timeout

Location: `omniNotes/src/androidTest/java/it/feio/android/omninotes/testutils/RetryableAssert.java:54` · Agents: quality

The equality condition is normally false immediately because endTime is in the future. An asynchronous condition that becomes true within the requested timeout still fails after only the initial attempt and final assertion.

Fix: Retry while the deadline has not passed, return immediately on success, and pause briefly between attempts using a monotonic clock.

Suggested test: Supply a condition that becomes true after 100 ms with a 1-second timeout and assert success; verify an always-false condition fails after the timeout.

Evidence:

````
    while (System.currentTimeMillis() == endTime);
````

## 23. [MEDIUM] Camera assertions cannot both succeed and may never run

Location: `omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/FabCameraNoteTest.java:93` · Agents: tests

An empty attachment list cannot have element zero. Furthermore, these assertions exist only in an EventBus callback; the test body never asserts that the callback occurred or waits for its result. Missing events can therefore leave the camera behavior unverified.

Fix: Capture the event, await it with a bounded synchronization mechanism, and assert the expected attachment count and MIME type on the test thread. Release Intents and unregister the subscriber in teardown.

Suggested test: Complete the stubbed camera capture and assert that an update arrives and contains exactly one image attachment. Suppress the update in a negative scenario and verify that the test fails on timeout.

Evidence:

````
    assertEquals(0, updatedNote.getAttachmentsList().size());
    assertEquals(Constants.MIME_TYPE_IMAGE, updatedNote.getAttachmentsList().get(0).getMime_type());
````

## 24. [MEDIUM] Camera test contains mutually incompatible attachment assertions

Location: `omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/FabCameraNoteTest.java:93` · Agents: quality

No attachment list can satisfy both statements. A nonempty list fails the first assertion; an empty list passes it and then throws IndexOutOfBoundsException. Every delivered note-update event therefore fails this validation.

Fix: Assert the expected successful camera attachment count before inspecting its MIME type, and ensure the test waits for that event.

Suggested test: Deliver an update containing one image attachment and assert that the camera test completes successfully.

Evidence:

````
    assertEquals(0, updatedNote.getAttachmentsList().size());
    assertEquals(Constants.MIME_TYPE_IMAGE, updatedNote.getAttachmentsList().get(0).getMime_type());
````

## 25. [MEDIUM] FAB action assertions never resolve the matched views

Location: `omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/FabLifecycleTest.java:69` · Agents: tests

Espresso onView returns a ViewInteraction without resolving the matcher. Checking that interaction for null therefore passes even when the checklist action is missing or hidden. The camera assertion has the same problem, so fabActionsTest does not verify either action's visibility.

Fix: Execute check(matches(isDisplayed())) on both interactions and verify collapse hides the actions.

Suggested test: Expand the FAB and assert checklist and camera views are displayed using Espresso checks. Collapse it and assert they are not displayed. Verify the expanded-state assertion fails if either action is hidden.

Evidence:

````
            isDisplayed()));
    assertNotNull(checklistFabAction);
````

## 26. [MEDIUM] Create-note UI test never verifies that the note was saved

Location: `omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/NoteLifecycleTest.java:74` · Agents: tests

The test ends after navigation without asserting any saved state. A regression that silently discards the title, content, or entire note can pass as long as the editing controls and navigation still work.

Fix: Assert the resulting note appears in the list and retains its values when reopened.

Suggested test: Create a note with title "Note title" and content "Note content", navigate up, assert exactly one saved note with those values, then reopen it and assert both editor fields.

Evidence:

````
    onView(withId(R.id.detail_content))
        .perform(scrollTo(), replaceText(content), closeSoftKeyboard());

    navigateUp();
  }
````

## 27. [MEDIUM] DashClock and Pushbullet cannot bind to their extension services

Location: `omniNotes/src/main/AndroidManifest.xml:287` · Agents: quality

DashClock runs under another application's UID and cannot bind to a service marked exported=false, even with the declared permission. PushBulletExtension has the same configuration at lines 308–311, preventing that integration as well.

Fix: Export the extension services intended for external applications while retaining their permission restrictions.

Suggested test: From clients holding the respective extension permissions, assert that both services can be discovered and bound.

Evidence:

````
    <service
      android:name=".extensions.ONDashClockExtension"
      android:icon="@drawable/ic_stat_literal_icon"
      android:label="@string/app_name"
      android:permission="com.google.android.apps.dashclock.permission.READ_EXTENSION_DATA"
      android:exported="false">
````

## 28. [MEDIUM] External extension services are inaccessible to their host apps

Location: `omniNotes/src/main/AndroidManifest.xml:308` · Agents: quality

Pushbullet runs under another UID and cannot bind to a service declared exported=false, even with the specified permission. The DashClock extension has the same declaration, so both advertised integrations are blocked.

Fix: Export the extension services while retaining their host-specific binding permissions.

Suggested test: Bind from a separate test app holding the required host permission and assert that binding succeeds; assert that a caller without that permission is denied.

Evidence:

````
    <service
      android:name="it.feio.android.omninotes.extensions.PushBulletExtension"
      android:permission="com.pushbullet.android.permission.READ_MESSAGING_EXTENSION_DATA"
      android:exported="false">
````

## 29. [MEDIUM] The address migration discards every note's trash status

Location: `omniNotes/src/main/assets/sql/upgrade-453.sql:23` · Agents: tests

The replacement table declares trashed, but the copy omits it. Migrated rows receive NULL instead of their existing trash status, and dropping notes_tmp permanently loses that state. The supplied reminder tests create fresh rows and cannot detect migration damage.

Fix: Include trashed in both the INSERT and SELECT column lists.

Suggested test: Seed the pre-migration table with trashed=1 and trashed=0 notes, run upgrade-453.sql, and assert both values and all existing note fields are preserved.

Evidence:

````
INSERT INTO notes(note_id, creation, last_modification, title, content, archived, alarm, latitude, longitude, category_id, locked, checklist)
SELECT note_id, creation, last_modification, title, content, archived, alarm, latitude, longitude, category_id, locked, checklist
FROM notes_tmp;
````

## 30. [MEDIUM] The table migration drops every note's trash status

Location: `omniNotes/src/main/assets/sql/upgrade-453.sql:23` · Agents: quality

The replacement schema includes trashed, but the copy omits it. Existing trash flags are replaced with NULL and the original table is deleted. Upgrading a database containing trashed notes therefore loses their trash state.

Fix: Include trashed in both the INSERT column list and the SELECT projection.

Suggested test: Migrate a database containing both trashed and active notes; assert that each note retains its original trashed value.

Evidence:

````
INSERT INTO notes(note_id, creation, last_modification, title, content, archived, alarm, latitude, longitude, category_id, locked, checklist)
SELECT note_id, creation, last_modification, title, content, archived, alarm, latitude, longitude, category_id, locked, checklist
FROM notes_tmp;
DROP TABLE notes_tmp; 
````

## 31. [MEDIUM] Reminder migration compares milliseconds against seconds

Location: `omniNotes/src/main/assets/sql/upgrade-482.sql:31` · Agents: quality

The supplied reminder tests store alarm timestamps in milliseconds, whereas strftime('%s', 'now') returns seconds. Adding 1000 does not convert units. Ordinary past reminders therefore fail this predicate and are not marked fired during migration.

Fix: Multiply the Unix timestamp by 1000 before comparing it with alarm.

Suggested test: Migrate notes with alarms one minute before and after the current time; assert that only the past alarm is marked fired.

Evidence:

````
UPDATE notes
SET reminder_fired = 1
WHERE alarm < (SELECT strftime('%s', 'now') + 1000);
````

## 32. [MEDIUM] All preferences, including authentication data, are logged

Location: `omniNotes/src/main/java/it/feio/android/omninotes/BaseActivity.java:76` · Agents: security

Every activity resume logs all preferences, which include password and recovery-answer entries defined in ConstantsBase. LogDelegate writes these messages to logcat or, when file logging is enabled, to public external storage. An attacker with access to those logs can obtain authentication material; other apps with shared-storage read access can read the public logs on applicable Android versions.

Fix: Remove the preference dump. Log only explicitly selected, nonsensitive diagnostic values.

Suggested test: Populate password and recovery-answer preferences with sentinel values, resume the activity with file logging enabled, and assert neither sentinel appears in captured logs or log files.

Evidence:

````
    LogDelegate.d(Prefs.getAll().toString());
````

## 33. [MEDIUM] Category color selection is lost on activity recreation

Location: `omniNotes/src/main/java/it/feio/android/omninotes/CategoryActivity.java:82` · Agents: quality

onColorSelection updates selectedColor but does not update category. Only category is saved, and onCreate restores selectedColor from category.getColor(). Rotating after choosing a color therefore discards that choice, and saving persists the old color.

Fix: Save and restore selectedColor explicitly or update the category's color when the selection changes.

Suggested test: Choose a different category color, recreate the activity, and save; assert that the chosen color remains displayed and is persisted.

Evidence:

````
  @Override
  public void onSaveInstanceState(Bundle outState) {
    outState.putParcelable("category", category);
    super.onSaveInstanceState(outState);
  }
````

## 34. [MEDIUM] Process Text reads a CharSequence extra as a String

Location: `omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:532` · Agents: quality

EXTRA_PROCESS_TEXT carries a CharSequence, which can be a styled text object rather than a String. getStringExtra can return null for that valid payload, and the immediate toString call then crashes the activity. A missing extra also crashes.

Fix: Read the value with getCharSequenceExtra and convert it to a String only after checking for null.

Suggested test: Launch ACTION_PROCESS_TEXT with a SpannableString payload and assert that its text becomes the note content without a crash.

Evidence:

````
      if (Intent.ACTION_PROCESS_TEXT.equals(i.getAction())){
        content = i.getStringExtra(Intent.EXTRA_PROCESS_TEXT).toString();
````

## 35. [MEDIUM] Changing a note's coordinates retains its previous address

Location: `omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:940` · Agents: quality

When a note already has an address and the user retrieves a different location, the coordinates change but the old address suppresses reverse geocoding. The note displays and retains the old place while opening the map at the new place. Removing a location also leaves the address intact, so adding another location reproduces this mismatch.

Fix: Invalidate the cached address when coordinates change or are removed, then resolve the address for the new coordinates.

Suggested test: Start with coordinates and address A, retrieve location B, and assert that address A is cleared and replaced by B's address or coordinates.

Evidence:

````
      noteTmp.setLatitude(location.getLatitude());
      noteTmp.setLongitude(location.getLongitude());
      if (!TextUtils.isEmpty(noteTmp.getAddress())) {
        binding.fragmentDetailContent.location.setVisibility(View.VISIBLE);
        binding.fragmentDetailContent.location.setText(noteTmp.getAddress());
````

## 36. [MEDIUM] Refreshing coordinates retains the previous location's address

Location: `omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:940` · Agents: tests

For a note with an existing address, retrieving a new location updates coordinates but reuses the old address and skips reverse geocoding. The displayed and persisted address can therefore describe a different place from the map destination.

Fix: Invalidate the cached address when coordinates change and resolve an address for the new coordinates.

Suggested test: Open a note with coordinates and address A, then deliver location B. Assert reverse geocoding receives B and the displayed and saved address becomes B's address, or B's coordinates when lookup fails.

Evidence:

````
      noteTmp.setLatitude(location.getLatitude());
      noteTmp.setLongitude(location.getLongitude());
      if (!TextUtils.isEmpty(noteTmp.getAddress())) {
        binding.fragmentDetailContent.location.setVisibility(View.VISIBLE);
        binding.fragmentDetailContent.location.setText(noteTmp.getAddress());
````

## 37. [MEDIUM] Completed playback abandons the MediaPlayer without releasing it

Location: `omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:1782` · Agents: quality

This is a resource leak. Each naturally completed playback clears the only field used by stopPlaying to release the player, without releasing mp. Repeatedly playing attachments accumulates native media resources until garbage collection and can exhaust playback resources.

Fix: Release mp in the completion callback before clearing the field, and release the player on preparation failures as well.

Suggested test: Complete playback repeatedly with a mocked MediaPlayer; assert release is called exactly once for every created player.

Evidence:

````
      mPlayer.setOnCompletionListener(mp -> {
        mPlayer = null;
````

## 38. [MEDIUM] Recording failures leave a recorder that Stop cannot safely stop

Location: `omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:1833` · Agents: quality

This is incomplete error recovery: isRecording is set before preparation, but this catch neither resets it nor releases mRecorder. If prepare fails, the next recording-button click calls stopRecording, whose unguarded mRecorder.stop() throws because recording never started. Stopping immediately after a successful start can also throw when insufficient audio has been captured.

Fix: Set isRecording only after start succeeds, release and clear the recorder on failure, and handle stop failures with cleanup in a finally block. Attach a recording only after a successful stop.

Suggested test: Simulate prepare throwing IOException, then click the recording control again; assert no crash, a released recorder, and no invalid attachment.

Evidence:

````
          try {
            audioRecordingTimeStart = Calendar.getInstance().getTimeInMillis();
            mRecorder.prepare();
            mRecorder.start();
          } catch (IOException | IllegalStateException e) {
            LogDelegate.e("prepare() failed", e);
            mainActivity.showMessage(R.string.error, ONStyle.ALERT);
          }
````

## 39. [MEDIUM] Removing all attachments disconnects the adapter from subsequent additions

Location: `omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:2018` · Agents: quality

The note and adapter receive different empty lists. Subsequent attachment callbacks add to noteTmp and notify the adapter, but the adapter still observes its separate empty list. Attachments added after Delete All therefore do not appear in the grid.

Fix: Construct the replacement adapter with noteTmp.getAttachmentsList(), as initViewAttachments does.

Suggested test: Delete all attachments, then add another attachment; assert that the grid displays the new attachment and the note contains it.

Evidence:

````
  private void removeAllAttachments() {
    noteTmp.setAttachmentsList(new ArrayList<>());
    mAttachmentAdapter = new AttachmentAdapter(mainActivity, new ArrayList<>());
    mGridView.invalidateViews();
    mGridView.setAdapter(mAttachmentAdapter);
  }
````

## 40. [MEDIUM] Gallery initialization indexes an explicitly permitted empty list

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

## 41. [MEDIUM] Opening media crashes when no viewer is installed

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

## 42. [MEDIUM] Temporary category navigation can crash new-note creation

Location: `omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:938` · Agents: quality

Java evaluates both arguments before calling defaultIfNull. When a widget supplies navigationTmp while the persistent navigation has no category, Navigation.getCategory().toString() can throw NullPointerException even though the temporary category is available. The surrounding catch handles only NumberFormatException.

Fix: Select the category ID with a conditional expression so Navigation.getCategory() is evaluated only when needed, and handle an absent category.

Suggested test: Open a category widget while persistent navigation is Notes, then create a note; assert that creation succeeds with the widget category.

Evidence:

````
        if (checkNavigation(Navigation.CATEGORY) || !isEmpty(mainActivity.navigationTmp)) {
          String categoryId = ObjectUtils.defaultIfNull(mainActivity.navigationTmp,
              Navigation.getCategory().toString());
````

## 43. [MEDIUM] Note updates always skip the final list item

Location: `omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:1190` · Agents: tests

IntStream.range excludes its upper bound, so the final note is never updated. With one note, no items are examined. NoteLocationTest posts a CategoriesUpdatedEvent after NotesUpdatedEvent, causing a full reload that masks this defect.

Fix: Use the list size as the exclusive upper bound and test NotesUpdatedEvent without a subsequent full reload.

Suggested test: Load a single note, post only NotesUpdatedEvent with changed title and location, and assert the adapter and displayed row contain the new values. Repeat for the last item of a multi-note list.

Evidence:

````
    notesUpdatedEvent.getNotes().stream().forEach(updatedNote ->
        IntStream.range(0, listAdapter.getNotes().size() - 1)
            .filter(i -> listAdapter.getItem(i).get_id().equals(updatedNote.get_id()))
````

## 44. [MEDIUM] Note updates always skip the last adapter item

Location: `omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:1190` · Agents: quality

IntStream.range excludes its upper bound. Subtracting one skips the final note, and a list containing one note processes no updates at all. Its displayed content and adapter model remain stale.

Fix: Use the list size as the exclusive upper bound.

Suggested test: Post an update for the only note and for the last note in a larger list; assert that each adapter item is replaced and notified.

Evidence:

````
    notesUpdatedEvent.getNotes().stream().forEach(updatedNote ->
        IntStream.range(0, listAdapter.getNotes().size() - 1)
            .filter(i -> listAdapter.getItem(i).get_id().equals(updatedNote.get_id()))
````

## 45. [MEDIUM] Undoing trash does not restore the canceled reminder

Location: `omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:1304` · Agents: quality

Trashing cancels reminders before the operation is committed. onUndo restores adapter items and clears the pending state without rescheduling their reminders. Trashing a note with a future reminder and pressing Undo therefore leaves the note active but its alarm canceled.

Fix: Defer reminder cancellation until trash is committed, or explicitly reschedule reminders when undoing trash.

Suggested test: Schedule a future reminder, trash the note, and undo; assert that the note remains active and its reminder is still scheduled.

Evidence:

````
      trackModifiedNotes(getSelectedNotes());
      for (Note note : getSelectedNotes()) {
        listAdapter.remove(note);
        ReminderHelper.removeReminder(OmniNotes.getAppContext(), note);
      }
````

## 46. [MEDIUM] Activity stops receiving events after its first stop

Location: `omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:162` · Agents: tests

Registration occurs only in onCreate, whereas onStop unregisters the activity. Returning to the same activity instance does not call onCreate, leaving its PasswordRemovedEvent and NotificationsGrantedEvent handlers disconnected. The supplied UI tests do not exercise this stop/start transition.

Fix: Pair registration and unregistration in matching lifecycle callbacks, such as onStart and onStop.

Suggested test: Launch MainActivity, move it through stopped and started states without recreating it, and assert that it is registered and handles a posted NotificationsGrantedEvent after returning.

Evidence:

````
  @Override
  protected void onStop() {
    super.onStop();
    EventBus.getDefault().unregister(this);
  }
````

## 47. [MEDIUM] MainActivity stops receiving events after its first stop

Location: `omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:162` · Agents: quality

Registration occurs only in onCreate. After opening another activity or backgrounding and returning, the same MainActivity resumes without registering again. Its PasswordRemovedEvent and NotificationsGrantedEvent handlers no longer run.

Fix: Pair registration in onStart with unregistration in onStop, or pair onCreate registration with onDestroy cleanup.

Suggested test: Stop and restart the same activity, post NotificationsGrantedEvent, and assert that its handler still executes.

Evidence:

````
  @Override
  protected void onStop() {
    super.onStop();
    EventBus.getDefault().unregister(this);
  }
````

## 48. [MEDIUM] Malformed VIEW intents crash the activity

Location: `omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:439` · Agents: quality

An ACTION_VIEW intent without data dereferences null here. With data present, the subsequent shortcut branch also parses an absent or nonnumeric id without handling NumberFormatException. MainActivity is exported, so either malformed input can terminate it.

Fix: Validate the URI, scheme, host, and numeric ID before dispatching; reject malformed input without throwing.

Suggested test: Deliver ACTION_VIEW with no data, an app URI without id, and id=abc; assert that none crashes or opens an unintended note.

Evidence:

````
    if (Intent.ACTION_VIEW.equals(i.getAction()) && i.getDataString()
        .startsWith(UrlCompleter.HASHTAG_SCHEME)) {
````

## 49. [MEDIUM] Sharing multiple missing attachments crashes

Location: `omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:563` · Agents: tests

getShareableAttachmentUri returns null for missing files, and those entries are skipped. If all attachments are missing, mimeTypes is empty and indexing element zero throws instead of handling the failure.

Fix: Handle an empty set of shareable attachments explicitly before selecting a MIME type or launching the chooser.

Suggested test: Share a note containing two attachments whose files are absent. Assert no exception and either a documented text-only share or an error with no chooser launch. Also test one missing and one valid attachment.

Evidence:

````
      if (mimeTypes.size() > 1) {
        shareIntent.setType("*/*");
      } else {
        shareIntent.setType((String) mimeTypes.keySet().toArray()[0]);
      }
````

## 50. [MEDIUM] Sharing multiple missing attachments indexes an empty collection

Location: `omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:563` · Agents: quality

When a note has multiple attachments and every file is missing, getShareableAttachmentUri returns null for each and mimeTypes remains empty. This branch throws ArrayIndexOutOfBoundsException after displaying the missing-file messages.

Fix: Handle an empty URI collection explicitly by aborting sharing or falling back to text-only sharing.

Suggested test: Share a note containing two missing attachment files and assert graceful handling without a crash.

Evidence:

````
      if (mimeTypes.size() > 1) {
        shareIntent.setType("*/*");
      } else {
        shareIntent.setType((String) mimeTypes.keySet().toArray()[0]);
      }
````

## 51. [MEDIUM] Asynchronous deletion events refresh drawer views on a worker thread

Location: `omniNotes/src/main/java/it/feio/android/omninotes/NavigationDrawerFragment.java:150` · Agents: quality

EventBus runs onEventAsync on a background thread. refreshMenus calls mDrawerToggle.syncState and executes CategoryMenuTask, whose onPreExecute immediately accesses drawer views and can add a footer. These UI operations therefore run off the main thread during note deletion, risking thread violations and inconsistent drawer updates.

Fix: Handle this event with onEventMainThread, keeping database work inside the tasks' background phases.

Suggested test: Post NotesDeletedEvent and assert that drawer synchronization and CategoryMenuTask.onPreExecute execute on the main looper.

Evidence:

````
  public void onEventAsync(NotesDeletedEvent event) {
    refreshMenus();
  }
````

## 52. [MEDIUM] Settings recreation overwrites restored navigation

Location: `omniNotes/src/main/java/it/feio/android/omninotes/SettingsActivity.java:64` · Agents: quality

After rotation or process recreation, FragmentManager restores the current settings fragment and its back stack. This unconditional replacement overwrites that restored screen with the root settings fragment while leaving the restored back stack in place, losing the user's location and making subsequent back navigation inconsistent.

Fix: Install the initial SettingsFragment only when savedInstanceState is null and otherwise retain FragmentManager's restored state.

Suggested test: Open a nested settings screen, recreate the activity, and assert that the same screen remains visible and Back returns to its parent.

Evidence:

````
    initUI();
    getSupportFragmentManager().beginTransaction()
        .replace(R.id.content_frame, new SettingsFragment()).commit();
````

## 53. [MEDIUM] Sketch save errors discard the drawing without informing the user

Location: `omniNotes/src/main/java/it/feio/android/omninotes/SketchFragment.java:206` · Agents: quality

This swallowed-exception pattern makes save return normally when opening or writing the file fails. MainActivity.handleBackPressed unconditionally pops the sketch immediately after save(), so a storage failure closes the editor and loses the user's drawing without a visible error.

Fix: Return a save result or propagate a specific failure, show an error, and navigate away only after confirmed successful writing. Check Bitmap.compress's result as well.

Suggested test: Use an unwritable output path, press Back, and assert that an error appears and the sketch remains available for retry.

Evidence:

````
      } catch (Exception e) {
        LogDelegate.e("Error writing sketch image data", e);
      }
````

## 54. [MEDIUM] Postponing a recurring reminder skips the selected occurrence

Location: `omniNotes/src/main/java/it/feio/android/omninotes/SnoozeActivity.java:137` · Agents: quality

ReminderPickers first calls onReminderPicked, which sets the alarm to the selected future time. This callback then calls setNextRecurrentReminder, whose helper searches after that alarm plus one minute. Selecting tomorrow at 09:00 with daily recurrence consequently saves the following day's 09:00 instead.

Fix: Save the selected alarm and recurrence directly when confirming the picker. Advance recurrence only when dismissing or completing a fired reminder.

Suggested test: Postpone a daily reminder to tomorrow at 09:00 and assert that the saved alarm is tomorrow at 09:00.

Evidence:

````
  public void onRecurrenceReminderPicked(String recurrenceRule) {
    if (note != null) {
      note.setRecurrenceRule(recurrenceRule);
      setNextRecurrentReminder(note);
````

## 55. [MEDIUM] Activity weak reference is dereferenced before the lifecycle guard

Location: `omniNotes/src/main/java/it/feio/android/omninotes/async/MainMenuTask.java:61` · Agents: quality

If the activity is destroyed and collected while the background task runs, mainActivity.get() returns null and onPostExecute crashes before reaching isAlive().

Fix: Resolve weak references once into local variables, validate the activity and fragment lifecycle first, and only then access the drawer.

Suggested test: Destroy the hosting activity before task completion and clear its weak reference; assert completion exits without accessing views or throwing.

Evidence:

````
    navDrawer = mainActivity.get().findViewById(R.id.drawer_nav_list);
    if (isAlive()) {
````

## 56. [MEDIUM] Main menu completion dereferences the activity before checking its lifecycle

Location: `omniNotes/src/main/java/it/feio/android/omninotes/async/MainMenuTask.java:61` · Agents: tests

The activity is held only through a WeakReference and can be collected while the task runs. onPostExecute dereferences it before the lifecycle guard, causing a NullPointerException instead of discarding the result.

Fix: Capture strong local references, validate both the activity and fragment lifecycle, and only then look up and update the drawer.

Suggested test: Delay menu construction, detach and destroy the host, and simulate a cleared activity reference before completion. Assert completion performs no view updates and throws no exception.

Evidence:

````
    navDrawer = mainActivity.get().findViewById(R.id.drawer_nav_list);
    if (isAlive()) {
````

## 57. [MEDIUM] Today's reminders are selected using UTC dates

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:653` · Agents: quality

SQLite evaluates both dates in UTC. In a non-UTC timezone, reminders near midnight can fall on a different local day, so getTodayReminders omits reminders due today and includes reminders due yesterday or tomorrow.

Fix: Compute the local day's start and next day's start in the application timezone and query the timestamp interval.

Suggested test: In Australia/Melbourne, query reminders around local midnight and assert only timestamps within the current local calendar day are returned.

Evidence:

````
        " WHERE DATE(" + KEY_REMINDER + "/1000, 'unixepoch') = DATE('now') AND " +
            KEY_TRASHED + " IS NOT 1";
````

## 58. [MEDIUM] Tag search interpolates input into executable SQL

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:763` · Agents: security

Tag values are inserted into SQL string literals without escaping or binding, and getNotes executes the resulting query with rawQuery. If an attacker can influence a searched tag, an apostrophe can cause an uncaught SQL error, while crafted SQL can alter the selection. The later regex filter runs only after SQL execution and cannot prevent injection.

Fix: Bind tag patterns through selection arguments, escaping LIKE metacharacters when literal matching is intended.

Suggested test: Search for tags containing apostrophes and SQL syntax; assert that they are treated literally, do not throw, and do not broaden the SQL selection.

Evidence:

````
      whereCondition.append(String.format("((%s IS 1 AND %s LIKE '%%%s%%') OR (%s is NOT 1 AND (%s LIKE '%%%s%%' OR %s LIKE '%%%s%%')))"
          , KEY_LOCKED, KEY_TITLE, tags[i], KEY_LOCKED, KEY_CONTENT, tags[i], KEY_TITLE, tags[i]));
````

## 59. [MEDIUM] Tag searches interpolate unescaped text into SQL

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:763` · Agents: tests

A tag containing an apostrophe breaks the SQL literal and can cause query failure. Tags are also inserted directly into Pattern.compile at line 774, so regex metacharacters can change matching or throw PatternSyntaxException. The supplied tag navigation test uses only #hashtag and does not assert search results.

Fix: Bind SQL arguments, escape LIKE metacharacters for literal matching, and quote tag text with Pattern.quote before building the regex.

Suggested test: Seed notes with literal tags containing an apostrophe and regex metacharacters, then call getNotesByTag with those values. Assert no exception and that only notes containing the exact requested tag are returned; include an empty tag array with explicitly defined behavior.

Evidence:

````
      whereCondition.append(String.format("((%s IS 1 AND %s LIKE '%%%s%%') OR (%s is NOT 1 AND (%s LIKE '%%%s%%' OR %s LIKE '%%%s%%')))"
          , KEY_LOCKED, KEY_TITLE, tags[i], KEY_LOCKED, KEY_CONTENT, tags[i], KEY_TITLE, tags[i]));
````

## 60. [MEDIUM] Tag values are interpolated directly into SQL

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:763` · Agents: quality

A tag argument containing an apostrophe produces malformed SQL and an uncaught database exception. Unlike getNotesByPattern, this method does not escape its input. SQL metacharacters can also change the query's meaning.

Fix: Pass tag patterns as bound selection arguments, escaping LIKE wildcards when literal matching is intended.

Suggested test: Search for a tag containing an apostrophe; assert the query completes and returns only literal matches.

Evidence:

````
      whereCondition.append(String.format("((%s IS 1 AND %s LIKE '%%%s%%') OR (%s is NOT 1 AND (%s LIKE '%%%s%%' OR %s LIKE '%%%s%%')))"
          , KEY_LOCKED, KEY_TITLE, tags[i], KEY_LOCKED, KEY_CONTENT, tags[i], KEY_TITLE, tags[i]));
````

## 61. [MEDIUM] Single-line SQL comments consume subsequent statements

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/SqlParser.java:63` · Agents: quality

The block-comment opener checks for a closing brace instead of */. A complete comment such as /* migration */ enters multiline-comment mode, and all following SQL is discarded until another line ends in */. A script can therefore silently omit its migration statements.

Fix: Recognize a closing */ on the opening line, preferably using a parser that tracks comment delimiters and preserves SQL outside them.

Suggested test: Parse '/* migration */\nCREATE TABLE example(id INTEGER);' and assert that the CREATE TABLE statement is returned.

Evidence:

````
            if (line.startsWith("/*")) {
              if (!line.endsWith("}")) {
                multiLineComment = "/*";
              }
````

## 62. [MEDIUM] Single-line SQL comments discard subsequent statements

Location: `omniNotes/src/main/java/it/feio/android/omninotes/db/SqlParser.java:63` · Agents: tests

The block-comment opener checks for a closing brace instead of */. A complete single-line comment consequently enters multiline-comment mode and causes following SQL statements to be discarded until another line ends with */.

Fix: Recognize the correct closing delimiter on the opening line and add parser regression tests.

Suggested test: Parse "/* migration */\nCREATE TABLE example (id INTEGER);" and assert exactly one statement containing the CREATE TABLE command. Retain a separate test for multiline comments like those in upgrade-451.sql.

Evidence:

````
            if (line.startsWith("/*")) {
              if (!line.endsWith("}")) {
                multiLineComment = "/*";
              }
````

## 63. [MEDIUM] Tomorrow reminders are classified by elapsed hours instead of calendar date

Location: `omniNotes/src/main/java/it/feio/android/omninotes/extensions/ONDashClockExtension.java:133` · Agents: quality

At 08:00 today, a reminder at 20:00 tomorrow is excluded because it is 36 hours away. Conversely, an unfired reminder from yesterday has a negative difference and is labeled tomorrow. Elapsed hours do not identify the next calendar day.

Fix: Compare the alarm's local calendar date with a Calendar advanced by one day, using a single captured current time.

Suggested test: Assert that tomorrow evening is included when now is this morning, yesterday is excluded, and classification remains correct across daylight-saving transitions.

Evidence:

````
        } else if (
            (Long.valueOf(note.getAlarm()) - Calendar.getInstance().getTimeInMillis()) / (1000 * 60
                *
                60) < 24) {
          tomorrow.add(note);
        }
````

## 64. [MEDIUM] Note export failures are swallowed

Location: `omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:78` · Agents: quality

This is the swallowed-exception anti-pattern. If storage fills or the provider fails while writing a note, exportNote returns normally and exportNotes continues without any failure result. Callers cannot distinguish a complete backup from one missing note contents.

Fix: Propagate the write failure or return an explicit result that exportNotes aggregates and reports as an incomplete backup.

Suggested test: Make a note write throw IOException and assert that the overall export reports failure and identifies the affected note.

Evidence:

````
    try {
      DocumentFileHelper.write(getAppContext(), noteFile, note.toJSON());
    } catch (IOException e) {
      LogDelegate.e(String.format("Error on note %s backup: %s",  note.get_id(), e.getMessage()));
    }
````

## 65. [MEDIUM] Attachments belonging to locked notes are exported without encryption

Location: `omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:140` · Agents: security

exportAttachments obtains all database attachments and copies their original bytes into the backup directory without checking note protection. Although exportNote encrypts locked-note content, its images, recordings, and other attachments remain readable to anyone who obtains access to the backup folder or its storage provider.

Fix: Encrypt attachments associated with protected notes using authenticated encryption, and record the encryption metadata needed for restoration.

Suggested test: Export a locked note with an attachment containing a known marker. Assert that the backup attachment does not expose the original bytes and can be restored only with the correct secret.

Evidence:

````
  private static void exportAttachment(DocumentFileCompat attachmentsDestination, Attachment attachment)
      throws BackupAttachmentException {
    try {
      var destinationAttachment = attachmentsDestination.createFile("",
          attachment.getUri().getLastPathSegment());
      DocumentFileHelper.copyFileTo(getAppContext(), new File(attachment.getUri().getPath()),
          destinationAttachment);
````

## 66. [MEDIUM] Unreadable backup notes become empty notes during import

Location: `omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:187` · Agents: quality

This is the error-as-success-value anti-pattern. An unreadable JSON file produces a non-null empty Note, which passes importNotes' non-null filter and reaches updateNote in importNote. An empty file likewise returns the newly constructed Note. Failed reads are consequently treated as successful note imports.

Fix: Reject empty content and propagate a descriptive import failure, or return null and explicitly report skipped files before any database update.

Suggested test: Import an empty file and a file whose read throws IOException. Assert that neither creates a database note and both are reported as failed.

Evidence:

````
    } catch (IOException e) {
      LogDelegate.e("Error parsing note json");
      return new Note();
    }
````

## 67. [MEDIUM] Missing attachment directory crashes restore

Location: `omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:199` · Agents: quality

findFile can return null when the backup contains no attachment directory, such as an incomplete or manually copied backup. Calling exists on that result throws NullPointerException instead of returning the intended failure result.

Fix: Check for null and verify that the entry is a directory before accessing its contents.

Suggested test: Restore from a backup without an attachment directory and assert that importAttachments returns false without throwing.

Evidence:

````
    var backupAttachmentsDir = backupDir.findFile(attachmentsDir.getName());
    if (!backupAttachmentsDir.exists()) {
      return false;
    }
````

## 68. [MEDIUM] Selected backup folders receive no persisted URI permissions

Location: `omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:273` · Agents: tests

Read and write permission flags are distinct bits, so their bitwise AND is zero. The call therefore does not persist either permission, leaving the saved backup URI unusable after its temporary grant expires.

Fix: Combine read and write flags with bitwise OR and intersect that mask with the permissions actually granted by the result intent.

Suggested test: Select a document tree with read and write grants, save it, and assert persistedUriPermissions contains that tree with both permissions. After restarting the app, assert the saved folder can still be listed and written.

Evidence:

````
    final int takeFlags = FLAG_GRANT_READ_URI_PERMISSION & FLAG_GRANT_WRITE_URI_PERMISSION;
    context.getContentResolver().takePersistableUriPermission(intent.getData(), takeFlags);
````

## 69. [MEDIUM] Location cache selection ignores how old the fix is

Location: `omniNotes/src/main/java/it/feio/android/omninotes/helpers/location/LocationManagerLocationProvider.java:118` · Agents: quality

The provider selects cached fixes solely by accuracy and getLocation immediately returns the selected fix without requesting an update. An accurate GPS fix from a previous trip therefore beats a recent network fix and can be attached to a new note as the device's current position.

Fix: Reject fixes older than a defined freshness threshold using elapsed realtime, consider recency when comparing fixes, and request an update when no sufficiently fresh fix exists.

Suggested test: Provide an old accurate GPS fix and a recent network fix; assert that the old fix is not returned as the current position.

Evidence:

````
      if (location != null && (bestLocation == null
          || location.getAccuracy() < bestLocation.getAccuracy())) {
        bestLocation = location;
      }
````

## 70. [MEDIUM] Location selection accepts arbitrarily stale cached fixes

Location: `omniNotes/src/main/java/it/feio/android/omninotes/helpers/location/LocationManagerLocationProvider.java:118` · Agents: tests

Cached locations are ranked only by accuracy, with no age check. getLocation() immediately returns the selected fix, so an old precise GPS fix can override a recent network fix and prevent requesting the current position. The supplied factory test only checks that a provider exists.

Fix: Reject expired fixes and consider recency when selecting among acceptable cached locations.

Suggested test: Supply a day-old GPS fix with 5-meter accuracy and a recent network fix with 50-meter accuracy. Assert the recent fix is selected. With only expired fixes, assert fresh updates are requested and timeout produces exactly one failure callback.

Evidence:

````
      if (location != null && (bestLocation == null
          || location.getAccuracy() < bestLocation.getAccuracy())) {
        bestLocation = location;
      }
````

## 71. [MEDIUM] Notification cancellation does not match the identity used by show

Location: `omniNotes/src/main/java/it/feio/android/omninotes/helpers/notifications/NotificationsHelper.java:207` · Agents: tests

show(long) posts notifications with a string tag and numeric ID 0, but cancel(int) and cancel() use the untagged cancellation overload. Consequently, show(42) followed by cancel(42), or show() followed by cancel(), leaves the posted notification active.

Fix: Use consistent tag and ID pairs for posting and cancellation, while preserving the separate untagged progress notification behavior if needed.

Suggested test: Post with show(42), cancel that notification, and assert its tagged entry is absent from active notifications. Repeat with show() and cancel(), and verify cancellation leaves an unrelated notification intact.

Evidence:

````
    mNotificationManager.notify(String.valueOf(id), 0, mBuilder.build());
````

## 72. [MEDIUM] Notification cancellation uses a different identity from posting

Location: `omniNotes/src/main/java/it/feio/android/omninotes/helpers/notifications/NotificationsHelper.java:207` · Agents: quality

show(long) posts notifications with a string tag and integer ID 0, but cancel(int) calls cancel(id), which addresses an untagged notification. Thus show(42) followed by cancel(42) leaves the notification visible. updateMessage(int) and finish(int) likewise post under a different identity.

Fix: Use one consistent tag/ID convention across posting, updating, finishing, and cancellation.

Suggested test: Post with show(42), update it, and cancel it; assert there is exactly one notification after updating and none after cancellation.

Evidence:

````
    mNotificationManager.notify(String.valueOf(id), 0, mBuilder.build());
````

## 73. [MEDIUM] Parcel round trips lose explicit note IDs

Location: `omniNotes/src/main/java/it/feio/android/omninotes/models/Note.java:169` · Agents: tests

Neither writeToParcel nor the parcel constructor serializes the note ID. A note with an explicitly assigned ID cannot reliably retain its identity across parcel transport. ParcelableUtilTest uses a default note and object equality, while IntentHelperTest reads the original intent extra without forcing parcel serialization; neither explicitly checks this case.

Fix: Serialize and restore the note ID symmetrically, and assert important fields individually in the round-trip test.

Suggested test: Create a note with ID 1234567890123 and a different creation timestamp. Marshall and unmarshall it using Note.CREATOR, then assert the restored ID equals 1234567890123 and the creation timestamp is unchanged.

Evidence:

````
  public void writeToParcel(Parcel parcel, int flags) {
    parcel.writeString(String.valueOf(getCreation()));
    parcel.writeString(String.valueOf(getLastModification()));
````

## 74. [MEDIUM] Empty-state observer ignores granular insertions and removals

Location: `omniNotes/src/main/java/it/feio/android/omninotes/models/views/RecyclerViewEmptySupport.java:32` · Agents: tests

The observer implements only onChanged. RecyclerView notifications such as notifyItemRemoved and notifyItemInserted invoke separate callbacks, so removing the last item or inserting the first item through these notifications leaves the empty-state visibility stale. Existing lifecycle tests largely exercise paths that explicitly call notifyDataSetChanged.

Fix: Recalculate empty-state visibility from range insertion and removal callbacks as well as onChanged.

Suggested test: Attach an adapter containing one item, remove it and call only notifyItemRemoved(0); assert the empty view is visible and the list is gone. Insert the first item with only notifyItemInserted(0) and assert the inverse.

Evidence:

````
    @Override
    public void onChanged() {
      Adapter<?> adapter = getAdapter();
````

## 75. [MEDIUM] Empty-state visibility ignores item insertions and removals

Location: `omniNotes/src/main/java/it/feio/android/omninotes/models/views/RecyclerViewEmptySupport.java:32` · Agents: quality

The observer only handles notifyDataSetChanged. RecyclerView dispatches notifyItemInserted and notifyItemRemoved to separate observer callbacks, so removing the final item or inserting the first item through granular notifications leaves the empty view and list visibility unchanged.

Fix: Extract the visibility update into a helper and invoke it from onChanged, onItemRangeInserted, and onItemRangeRemoved.

Suggested test: Remove the only item using notifyItemRemoved and assert that the empty view appears; insert an item using notifyItemInserted and assert that the list reappears.

Evidence:

````
    @Override
    public void onChanged() {
      Adapter<?> adapter = getAdapter();
````

## 76. [MEDIUM] Queued alarms can overwrite a trashed note with stale data

Location: `omniNotes/src/main/java/it/feio/android/omninotes/receiver/AlarmReceiver.java:55` · Agents: tests

The guard only checks existence. A queued broadcast serialized before trashing still passes because the database row exists, then displays a notification and writes its old, untrashed state through updateNote(). The supplied receiver test covers deletion only, so it misses this path and stale edits to existing notes.

Fix: Load the current database note, reject trashed notes and obsolete alarms, and apply reminder changes to current data.

Suggested test: Serialize an active reminded note, trash and save it, then deliver the original broadcast. Assert the database note remains trashed, no notification appears, and no recurrent alarm is scheduled. Also edit the title after serialization and assert delivery preserves the edit.

Evidence:

````
        if (isNoteGone(note)) {
          LogDelegate.d("Reminder fired for a note that no longer exists, skipping");
          return;
        }
        createNotification(mContext, note);
        SnoozeActivity.setNextRecurrentReminder(note);
        updateNote(note);
````

## 77. [MEDIUM] Downloads URI parsing assumes document IDs are numeric

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/FileHelper.java:67` · Agents: quality

Downloads document IDs can contain prefixes such as raw: or msf:. Passing such a valid document URI to getPath throws NumberFormatException before reaching getDataColumn's error handling, interrupting file selection.

Fix: Handle supported document-ID forms explicitly and use ContentResolver streams when a document has no usable filesystem path.

Suggested test: Pass Downloads document URIs with numeric, raw:, and msf: IDs; assert that supported forms resolve and unsupported forms return a controlled result without throwing.

Evidence:

````
        final Uri contentUri = ContentUris
            .withAppendedId(Uri.parse("content://downloads/public_downloads"),
                parseLong(DocumentsContract.getDocumentId(uri)));
````

## 78. [MEDIUM] Denied exact-alarm access launches settings from an application context

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/ReminderHelper.java:63` · Agents: tests

SaveNoteTask supplies OmniNotes.getAppContext(). When exact-alarm access is denied on Android 12+, startActivity() lacks FLAG_ACTIVITY_NEW_TASK and throws from that application context. The reminder tests assume scheduling succeeds and do not exercise denied access.

Fix: Handle permission requests through an activity, or add the required task flag when launching from an application context and provide a way to retry scheduling after access is granted.

Suggested test: On API 31+, simulate canScheduleExactAlarms() returning false and call addReminder with an application context. Assert no exception, the settings intent has FLAG_ACTIVITY_NEW_TASK, and no alarm is scheduled before permission is granted.

Evidence:

````
        if (!alarmManager.canScheduleExactAlarms()) {
          Intent intent = new Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM);
          context.startActivity(intent);
          return;
        }
````

## 79. [MEDIUM] Exact-alarm permission requests crash when using the application context

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/ReminderHelper.java:63` · Agents: quality

SaveNoteTask and AlarmRestoreOnRebootService call this helper with the application context. When exact-alarm access is unavailable on Android 12 or later, starting this activity without FLAG_ACTIVITY_NEW_TASK throws instead of handling the missing permission.

Fix: Move permission prompting to an activity and return a scheduling failure to background callers, or use the required activity flag when an application-context launch is appropriate.

Suggested test: Deny exact-alarm access and schedule a future reminder through SaveNoteTask; assert that the operation reports missing access without throwing.

Evidence:

````
        if (!alarmManager.canScheduleExactAlarms()) {
          Intent intent = new Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM);
          context.startActivity(intent);
          return;
        }
````

## 80. [MEDIUM] DES encryption provides only a 56-bit effective key

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:58` · Agents: security

An attacker who obtains ciphertext produced by this helper can attack DES's 56-bit effective key offline. DESKeySpec also uses only the first eight password bytes, so longer passwords do not increase key strength. The snapshot does not show which data uses this helper.

Fix: Use authenticated encryption such as AES-GCM with a randomly generated nonce and a suitable password-based key derivation function. Version the ciphertext format to support migration.

Suggested test: Verify that the replacement produces different ciphertext for repeated encryption of identical inputs, rejects tampering, and derives different keys when password bytes beyond the eighth byte change.

Evidence:

````
                val keySpec = DESKeySpec(password.toByteArray(StandardCharsets.UTF_8))
                val keyFactory = SecretKeyFactory.getInstance("DES")
                val key = keyFactory.generateSecret(keySpec)
                val clearText = value.toByteArray(StandardCharsets.UTF_8)
                // Cipher is not thread safe
                val cipher = Cipher.getInstance("DES")
````

## 81. [MEDIUM] Password-based encryption uses a truncated DES key

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:58` · Agents: security

DES provides only a 56-bit effective key, and DESKeySpec uses only the first eight password bytes. An attacker who obtains ciphertext can attack this limited key space offline; longer password suffixes provide no additional protection. No password derivation salt or work factor is used. Actual callers and protected data are absent from the snapshot.

Fix: Use authenticated encryption such as AES-GCM with a random nonce and a key derived using a salted password KDF with an appropriate work factor. Provide a migration path for existing ciphertext.

Suggested test: Verify the replacement uses distinct salts and nonces for repeated encryption, rejects modified ciphertext, and does not treat passwords sharing their first eight bytes as equivalent.

Evidence:

````
                val keySpec = DESKeySpec(password.toByteArray(StandardCharsets.UTF_8))
                val keyFactory = SecretKeyFactory.getInstance("DES")
                val key = keyFactory.generateSecret(keySpec)
                val clearText = value.toByteArray(StandardCharsets.UTF_8)
                // Cipher is not thread safe
                val cipher = Cipher.getInstance("DES")
````

## 82. [MEDIUM] Encryption failures return the original plaintext

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66` · Agents: tests

An encryption error is represented as a successful string result containing the sensitive input. For example, a password shorter than eight UTF-8 bytes makes DESKeySpec fail. The supplied locked-note backup tests use valid long passwords and do not exercise this failure path.

Fix: Return an explicit failure or throw an exception, and require callers to abort saving encrypted content on failure.

Suggested test: Call encrypt with plaintext "private note" and password "short"; assert an explicit failure is reported and plaintext cannot be accepted as encrypted output.

Evidence:

````
            } catch (e: Exception) {
                LogDelegate.e("Something is gone wrong encrypting", e)
                value
            }
````

## 83. [MEDIUM] Encryption failures silently export protected content as plaintext

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66` · Agents: tests

Encryption reports failure by returning the original plaintext. BackupHelper.exportNote assigns this result to a locked note's content and writes it to JSON without detecting failure. For example, an empty password produces an invalid DES key and allows protected content to be exported unencrypted.

Fix: Propagate encryption failure and abort the affected export with an explicit failure result instead of returning plaintext.

Suggested test: Export a locked note containing a unique secret with an empty password preference. Assert export reports failure and no backup JSON contains the plaintext secret. Also assert the original note content remains unchanged.

Evidence:

````
            } catch (e: Exception) {
                LogDelegate.e("Something is gone wrong encrypting", e)
                value
            }
````

## 84. [MEDIUM] Encryption failures silently persist plaintext

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

## 85. [MEDIUM] Encryption failures silently return plaintext

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66` · Agents: security

Any encryption exception returns the original sensitive content as a successful string result. For example, a password shorter than eight UTF-8 bytes causes DESKeySpec construction to fail. A caller storing the result as protected note content can consequently persist plaintext without detecting the loss of confidentiality.

Fix: Propagate an explicit encryption failure and require callers to abort saving protected content when encryption fails.

Suggested test: Call encrypt with sensitive content and a password shorter than eight bytes; assert an explicit failure and verify that the saving flow does not persist plaintext.

Evidence:

````
            } catch (e: Exception) {
                LogDelegate.e("Something is gone wrong encrypting", e)
                value
            }
````

## 86. [MEDIUM] Attachment copy failures are reported as success

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:127` · Agents: quality

The copyFile overload catches IOException and returns false, but this caller ignores that result. A read failure or full storage therefore returns a partial file as a valid attachment, and the surrounding IOException fallback never runs for the copy failure.

Fix: Check the result or use a throwing copy operation. Delete partial output and return failure before constructing an Attachment.

Suggested test: Use an input stream that throws after several bytes; assert that attachment creation fails and leaves no partial attachment file.

Evidence:

````
      contentResolverInputStream = mContext.getContentResolver().openInputStream(uri);
      contentResolverOutputStream = new FileOutputStream(file);
      copyFile(contentResolverInputStream, contentResolverOutputStream);
````

## 87. [MEDIUM] Attachment import ignores copy failures

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:127` · Agents: tests

The stream copy helper catches IOException and returns false, but this caller ignores that result. A mid-copy failure therefore bypasses the fallback handling and returns the partial file as a successful import; createAttachmentFromUri can then construct an attachment for corrupted data.

Fix: Propagate or check copy failure, delete the partial destination, and return failure rather than constructing an attachment.

Suggested test: Use a content provider whose stream emits a few bytes and then throws IOException. Assert createAttachmentFromUri returns null and leaves no partial attachment file.

Evidence:

````
      contentResolverInputStream = mContext.getContentResolver().openInputStream(uri);
      contentResolverOutputStream = new FileOutputStream(file);
      copyFile(contentResolverInputStream, contentResolverOutputStream);
````

## 88. [MEDIUM] Attachment names can collide within the same millisecond

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:248` · Agents: quality

Synchronization serializes calls but does not make timestamps unique. Two attachments with the same extension created within one millisecond receive the same path. FileOutputStream then truncates the earlier attachment, so both notes can reference the later file.

Fix: Reserve unique files atomically with File.createTempFile or use collision-resistant names with exclusive creation.

Suggested test: Create multiple attachment files with a fixed clock and identical extensions; assert distinct paths and preserved contents.

Evidence:

````
  private static synchronized String createNewAttachmentName(String extension) {
    Calendar now = Calendar.getInstance();
    SimpleDateFormat sdf = new SimpleDateFormat(Constants.DATE_FORMAT_SORTABLE);
    String name = sdf.format(now.getTime());
    name += extension != null ? extension : "";
    return name;
  }
````

## 89. [MEDIUM] Backup copying leaks its output stream and hides failure

Location: `omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:272` · Agents: quality

This resource-leak pattern opens a FileOutputStream that neither this method nor copyFile closes. Repeated backup copies can exhaust file descriptors. The ignored copy result and unconditional destination return also present incomplete or nonexistent backups as successful.

Fix: Own the output stream with try-with-resources and propagate copy/open failures or return an explicit failure after deleting partial output.

Suggested test: Force a copy IOException and assert failure rather than a destination result; verify the output stream closes on success and failure.

Evidence:

````
    try {
      copyFile(fileInputStream, new FileOutputStream(destination));
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    }
    return destination;
````

## 90. [MEDIUM] Widget display preferences are shared globally and lost on restart

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

## 91. [MEDIUM] Widget fill-in intents expose decrypted locked notes to the host

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

## 92. [LOW] Exception wrapper discards the original cause

Location: `omniNotes/src/androidTest/java/it/feio/android/omninotes/exceptions/TestException.java:26` · Agents: quality

This lost-cause exception-wrapping pattern ignores the supplied exception. A wrapped setup or I/O failure loses its message and original stack trace, obscuring the reason the test failed.

Fix: Call super(e) or super(message, e) to preserve the cause.

Suggested test: Construct TestException with an IOException and assert that getCause() returns that same exception.

Evidence:

````
  public TestException(Exception e) {

  }
````

## 93. [LOW] FAB action assertions never resolve the matching views

Location: `omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/FabLifecycleTest.java:70` · Agents: quality

Espresso onView creates a ViewInteraction without resolving its matcher. Checking that wrapper for null does not verify that the checklist action exists or is displayed. The camera assertion at line 81 has the same problem, so the test passes even when both action views are missing.

Fix: Call check(matches(isDisplayed())) on each ViewInteraction so Espresso resolves and validates the views.

Suggested test: Hide or remove either action view and assert that fabActionsTest fails.

Evidence:

````
    assertNotNull(checklistFabAction);
````

## 94. [LOW] Google Play availability assertion cannot detect an incorrect result

Location: `omniNotes/src/androidTest/java/it/feio/android/omninotes/utils/MiscUtilsTest.kt:29` · Agents: tests

Checking the result's Boolean type does not verify availability behavior. An implementation that always returns true or always returns false can pass this test.

Fix: Control the availability dependency and assert the expected Boolean value for each relevant state.

Suggested test: Arrange Google Play services as available and assert true; arrange services as missing or unavailable and assert false.

Evidence:

````
        assertTrue(MiscUtils.isGooglePlayAvailable(testContext) is Boolean)
````

## 95. [LOW] Comma-tag test supplies an invalid selection and checks unchanged input

Location: `omniNotes/src/test/java/it/feio/android/omninotes/utils/TagsHelperTest.java:123` · Agents: tests

The selection includes index 1 although the list contains only index 0. Also, the returned tag text is never applied to the note before retrieval, so the final absence assertion checks a note that never contained the comma tag. It does not establish comma parsing behavior.

Fix: Select only index 0 and apply the returned text to the note before checking retrieval.

Suggested test: Add "#comma,comma" using selection {0}, append the returned text to the note, and assert the exact intended parsed tag set. Test invalid selection indices separately if supported.

Evidence:

````
    List<Tag> tags = new ArrayList<>();
    tags.add(new Tag(newTag, 1));
    Pair<String, List<Tag>> newTags = TagsHelper.addTagToNote(tags, new Integer[]{0, 1}, note);
    Map<String, Integer> tags1 = TagsHelper.retrieveTags(note);
````

## Review limitations

- quality: ok
  - Review was limited to the supplied snapshot; no tools or execution were used.
  - BaseNote, DbHelper, adapter implementations, build configuration, and other referenced dependencies were not supplied, limiting conclusions about identity, copying, database behavior, and platform compatibility.
- security: ok
  - Review was limited to the supplied snapshot; no tools or execution were used.
  - Encryption call sites, StorageHelper, MainActivity intent routing, notification formatting helpers, dependency versions, and FileProvider path configuration were not supplied, limiting assessment of reachability and downstream impact.
- tests: ok
  - Static review only; no tools were used and no tests were executed.
  - Database helpers, base models, location factory, several tested implementations, and shared test setup were not supplied. Their behavior and any additional tests could not be verified.
  - The migration finding applies when upgrade-453.sql is executed against an existing database.
- quality: ok
  - Review was limited to the supplied snapshot; no tools or execution were used.
  - Implementations of DbHelper, Navigation, NoteAdapter, BaseNote, and reminder processors were not supplied, limiting verification of dependent behavior and migration sequencing.
- security: ok
  - Review was limited to the supplied snapshot; no code was executed.
  - Production encryption callers, backup implementations, authentication helpers, dependency versions, and FileProvider path configuration were not supplied, so their protections and exploit reachability could not be verified.
- tests: ok
  - Static review only; no tools were called and no tests were run.
  - Several production helpers, adapters, base test classes, and dependency implementations are absent, limiting verification of test isolation and helper behavior.
  - Navigation resources and navigateTo implementation are absent, so the destination used by the trash lifecycle tests cannot be confirmed.
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
- quality: ok
  - Review was limited to the supplied snapshot; no tools or execution were used.
  - Missing helper implementations, base models, service code, resources, and dependency configuration limit assessment of database, serialization, storage, and lifecycle behavior.
- security: ok
  - Review was limited to the supplied snapshot; no tools or execution were used.
  - Missing intent handlers, storage helpers, database implementation, and provider path configuration prevent confirming additional exploit paths.
- tests: ok
  - Review was limited to the supplied snapshot; no tools were called and no tests were run.
  - Several helper implementations, BaseNote, BaseEspressoTest, dependency configuration, and resources were not supplied, limiting assessment of their behavior and test setup.
  - Suggested tests describe missing assertions and failure scenarios, not measured coverage.
- quality: ok
  - Static review only; no tools, execution, or external verification were used.
  - Missing superclass implementations, helper implementations, build properties, and merged manifests limit verification of downstream behavior and platform compatibility.
- security: ok
  - Review was limited to the supplied snapshot; no tools or execution were used.
  - Password storage format, encryption callers, DetailFragment authorization, and FileProvider path configuration were not supplied.
  - Dependency vulnerability status and resolved transitive versions could not be verified.
- tests: ok
  - Review was limited to the supplied snapshot; no tools were called and no tests were executed.
  - Several production dependencies and test fixtures, including DbHelper, BaseAndroidTestCase, FileProviderHelper, and the commons models, were not supplied, limiting verification of their behavior.
