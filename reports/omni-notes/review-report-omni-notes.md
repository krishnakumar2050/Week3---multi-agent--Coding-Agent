# Omni-Notes Android — comprehensive prioritized review

## Executive assessment

The review completed across five bounded batches: **15 successful specialist executions**, covering **263 unique source/configuration files (1,007,422 bytes)**. All agents reported actual model **gpt-6.1-sol** through the signed-in Codex backend. Keenable enrichment succeeded for Agent 1 in all five batches.

The engine retained **95 raw findings** (19 high, 72 medium, four low). Semantic consolidation produced **60 issue groups**: **59 source-supported static assessments** and **one deferred identity/Parcelable claim** requiring external dependency verification. Consolidated severity counts excluding that deferred claim: **9 high, 47 medium, 3 low**. These are not runtime-confirmed defects.

Prioritize destructive migration error handling, password-setting authorization, stored key material and sensitive logging, fail-open encryption, attachment identity, database transaction cleanup, and backup permission persistence.

## Scope and reproducibility

- Local repository: `/Users/krishnakumar/Documents/github/Omni-Notes`.
- Upstream: https://github.com/federicoiosue/Omni-Notes
- Reviewed revision: `504253db6781a19d377ab04153f2f2cd75ef5494`; checkout clean at review start.
- Selected scope: all 214 Java and 18 Kotlin files, SQL migrations, Gradle/build-support source selected by the extension allowlist, Android manifests, and resource XML under res/xml. The exact selection is in [scope.json](scope.json).
- Layouts, translated strings, drawable assets, binary dependencies, and generated output were not comprehensively reviewed.
- Five size-balanced snapshots of approximately 223 KB each. Note, Security, Constants, and manifest context were repeated where selected. Other cross-batch dependencies may be missed.
- Existing unit and Android instrumentation tests were included; unlike the earlier Swift sample, this repository has a test suite. Assertions about missing coverage are provisional because each specialist saw only one batch.
- No Gradle build, Android emulator/device run, unit/instrumentation test execution, exploit reproduction, or measured coverage was performed.
- Fireworks credentials were unavailable locally; review used the existing ChatGPT-authenticated Codex adapter.
- The engine gained Kotlin and Gradle source selection plus Kotlin knowledge-query support. Its 135 local tests and lint checks passed. Omni-Notes source was not modified.

## Priority index

P1: address before release, migration rollout, or reliance on the affected protection/backup feature. P2: next correctness/security remediation wave. P3: test reliability improvements. VERIFY: exclude from confirmed defect counts until dependency behavior is established. Priority is an editorial remediation order; severity preserves the highest agent rating in the group.

| ID | Priority | Severity | Issue | Location |
| --- | --- | --- | --- | --- |
| ON-01 | P1 | HIGH | Migration errors are swallowed before destructive statements continue | [DbHelper.java:283](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:283) |
| ON-02 | P1 | HIGH | Application password protection can be disabled without authentication | [SettingsFragment.java:335](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/SettingsFragment.java:335) |
| ON-03 | P1 | HIGH | Stored password verifier also serves as the note decryption key | [DbHelper.java:473](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:473) |
| ON-04 | P1 | MEDIUM | All preferences, including authentication data, are logged | [BaseActivity.java:76](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/BaseActivity.java:76) |
| ON-05 | P1 | HIGH | Cryptographic failures silently return unprocessed content | [Security.kt:66](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66) |
| ON-06 | P1 | HIGH | Backup encryption truncates the password hash to a weak DES key | [Security.kt:58](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:58) |
| ON-07 | P1 | HIGH | Duplicate-creation migration can preserve duplicates and update multiple notes | [UpgradeProcessor.java:171](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/async/upgrade/UpgradeProcessor.java:171) |
| ON-08 | P1 | HIGH | Millisecond attachment IDs can overwrite other attachments | [DbHelper.java:306](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:306) |
| ON-09 | P1 | HIGH | Note updates leave transactions open when an operation throws | [DbHelper.java:266](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:266) |
| ON-10 | P1 | HIGH | Persistable folder permission flags always evaluate to zero | [BackupHelper.java:273](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:273) |
| ON-11 | P2 | MEDIUM | Widget fill-in intents expose decrypted locked notes to the host | [ListRemoteViewsFactory.java:127](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/widget/ListRemoteViewsFactory.java:127) |
| ON-12 | P2 | MEDIUM | Attachments belonging to locked notes are exported without encryption | [BackupHelper.java:140](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:140) |
| ON-13 | P2 | MEDIUM | Note export failures are swallowed | [BackupHelper.java:78](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:78) |
| ON-14 | P2 | MEDIUM | Unreadable backup notes become empty notes during import | [BackupHelper.java:187](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:187) |
| ON-15 | P2 | MEDIUM | Missing attachment directory crashes restore | [BackupHelper.java:199](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:199) |
| ON-16 | P2 | MEDIUM | The address migration discards every note's trash status | [upgrade-453.sql:23](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/assets/sql/upgrade-453.sql:23) |
| ON-17 | P2 | MEDIUM | Reminder migration compares milliseconds against seconds | [upgrade-482.sql:31](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/assets/sql/upgrade-482.sql:31) |
| ON-18 | P2 | MEDIUM | Tag search interpolates input into executable SQL | [DbHelper.java:763](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:763) |
| ON-19 | P2 | MEDIUM | Single-line SQL comments consume subsequent statements | [SqlParser.java:63](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/SqlParser.java:63) |
| ON-20 | P2 | MEDIUM | Attachment copy failures are reported as success | [StorageHelper.java:127](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:127) |
| ON-21 | P2 | MEDIUM | Attachment names can collide within the same millisecond | [StorageHelper.java:248](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:248) |
| ON-22 | P2 | MEDIUM | Backup copying leaks its output stream and hides failure | [StorageHelper.java:272](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:272) |
| ON-23 | P2 | MEDIUM | Queued alarms can overwrite a trashed note with stale data | [AlarmReceiver.java:55](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/receiver/AlarmReceiver.java:55) |
| ON-24 | P2 | MEDIUM | Denied exact-alarm access launches settings from an application context | [ReminderHelper.java:63](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/ReminderHelper.java:63) |
| ON-25 | P2 | MEDIUM | Postponing a recurring reminder skips the selected occurrence | [SnoozeActivity.java:137](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/SnoozeActivity.java:137) |
| ON-26 | P2 | MEDIUM | Today's reminders are selected using UTC dates | [DbHelper.java:653](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:653) |
| ON-27 | P2 | MEDIUM | Tomorrow reminders are classified by elapsed hours instead of calendar date | [ONDashClockExtension.java:133](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/extensions/ONDashClockExtension.java:133) |
| ON-28 | P2 | MEDIUM | Activity stops receiving events after its first stop | [MainActivity.java:162](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:162) |
| ON-29 | P2 | MEDIUM | Malformed VIEW intents crash the activity | [MainActivity.java:439](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:439) |
| ON-30 | P2 | MEDIUM | Sharing multiple missing attachments crashes | [MainActivity.java:563](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:563) |
| ON-31 | P2 | MEDIUM | Sketch save errors discard the drawing without informing the user | [SketchFragment.java:206](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/SketchFragment.java:206) |
| ON-32 | P2 | MEDIUM | Recording failures leave a recorder that Stop cannot safely stop | [DetailFragment.java:1833](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:1833) |
| ON-33 | P2 | MEDIUM | Completed playback abandons the MediaPlayer without releasing it | [DetailFragment.java:1782](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:1782) |
| ON-34 | P2 | MEDIUM | Process Text reads a CharSequence extra as a String | [DetailFragment.java:532](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:532) |
| ON-35 | P2 | MEDIUM | Downloads URI parsing assumes document IDs are numeric | [FileHelper.java:67](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/FileHelper.java:67) |
| ON-36 | P2 | MEDIUM | Gallery initialization indexes an explicitly permitted empty list | [GalleryActivity.java:163](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/GalleryActivity.java:163) |
| ON-37 | P2 | MEDIUM | Opening media crashes when no viewer is installed | [GalleryActivity.java:190](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/GalleryActivity.java:190) |
| ON-38 | P2 | MEDIUM | Temporary category navigation can crash new-note creation | [ListFragment.java:938](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:938) |
| ON-39 | P2 | MEDIUM | Activity weak reference is dereferenced before the lifecycle guard | [MainMenuTask.java:61](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/async/MainMenuTask.java:61) |
| ON-40 | P2 | MEDIUM | Asynchronous deletion events refresh drawer views on a worker thread | [NavigationDrawerFragment.java:150](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/NavigationDrawerFragment.java:150) |
| ON-41 | P2 | MEDIUM | Note updates always skip the final list item | [ListFragment.java:1190](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:1190) |
| ON-42 | P2 | MEDIUM | Undoing trash does not restore the canceled reminder | [ListFragment.java:1304](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:1304) |
| ON-43 | P2 | MEDIUM | Removing all attachments disconnects the adapter from subsequent additions | [DetailFragment.java:2018](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:2018) |
| ON-44 | P2 | MEDIUM | Changing a note's coordinates retains its previous address | [DetailFragment.java:940](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:940) |
| ON-45 | P2 | MEDIUM | Location cache selection ignores how old the fix is | [LocationManagerLocationProvider.java:118](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/location/LocationManagerLocationProvider.java:118) |
| ON-46 | P2 | MEDIUM | Notification cancellation does not match the identity used by show | [NotificationsHelper.java:207](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/notifications/NotificationsHelper.java:207) |
| ON-47 | P2 | MEDIUM | Empty-state observer ignores granular insertions and removals | [RecyclerViewEmptySupport.java:32](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/models/views/RecyclerViewEmptySupport.java:32) |
| ON-48 | P2 | MEDIUM | Category color selection is lost on activity recreation | [CategoryActivity.java:82](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/CategoryActivity.java:82) |
| ON-49 | P2 | MEDIUM | Settings recreation overwrites restored navigation | [SettingsActivity.java:64](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/SettingsActivity.java:64) |
| ON-50 | P2 | MEDIUM | Widget display preferences are shared globally and lost on restart | [ListRemoteViewsFactory.java:65](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/widget/ListRemoteViewsFactory.java:65) |
| ON-51 | P2 | MEDIUM | DashClock and Pushbullet cannot bind to their extension services | [AndroidManifest.xml:287](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/AndroidManifest.xml:287) |
| ON-52 | P3 | MEDIUM | Retry loop exits before the timeout | [RetryableAssert.java:54](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/testutils/RetryableAssert.java:54) |
| ON-53 | P3 | MEDIUM | Camera assertions cannot both succeed and may never run | [FabCameraNoteTest.java:93](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/FabCameraNoteTest.java:93) |
| ON-54 | P3 | MEDIUM | FAB action assertions never resolve the matched views | [FabLifecycleTest.java:69](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/FabLifecycleTest.java:69) |
| ON-55 | P3 | MEDIUM | Create-note UI test never verifies that the note was saved | [NoteLifecycleTest.java:74](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/NoteLifecycleTest.java:74) |
| ON-56 | P3 | MEDIUM | Upgrade assertion also passes if migration deletes attachments | [UpgradeProcessorTest.kt:41](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/async/upgrade/UpgradeProcessorTest.kt:41) |
| ON-57 | P3 | LOW | Exception wrapper discards the original cause | [TestException.java:26](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/exceptions/TestException.java:26) |
| ON-58 | P3 | LOW | Google Play availability assertion cannot detect an incorrect result | [MiscUtilsTest.kt:29](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/utils/MiscUtilsTest.kt:29) |
| ON-59 | P3 | LOW | Comma-tag test supplies an invalid selection and checks unchanged input | [TagsHelperTest.java:123](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/test/java/it/feio/android/omninotes/utils/TagsHelperTest.java:123) |
| ON-60 | VERIFY | Unconfirmed (high) | Note parceling loses the database ID | [Note.java:169](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/models/Note.java:169) |

## Detailed findings

### ON-01. [P1] Migration errors are swallowed before destructive statements continue

Severity: HIGH (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 3. Raw finding IDs: 6, 7.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:283](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:283).

**Assessment / preconditions:** Source inspection confirms execSqlFile logs an exception and continues. The data-loss example concerns legacy migration paths such as upgrade-501; an ordinary launch without that migration does not itself reproduce this failure.

**Agent-reported impact:** This is the swallowed-exception anti-pattern. In upgrade-501.sql, if copying notes fails because two existing notes share a creation timestamp, execution still reaches DROP TABLE notes_tmp. The upgrade can then complete and commit after deleting the original notes.

**Recommended fix:** Propagate SQL failures so SQLiteOpenHelper rolls back the upgrade transaction and preserves the original database.

**Suggested regression test:** Upgrade a database containing duplicate creation timestamps; assert the upgrade fails and all original notes remain available.

**Exact source excerpt:**

````
      try {
        db.execSQL(sqlInstruction);
      } catch (Exception e) {
        LogDelegate.e("Error executing command: " + sqlInstruction, e);
      }
````

### ON-02. [P1] Application password protection can be disabled without authentication

Severity: HIGH (highest agent rating). Status: source_supported_static_assessment. Agents: quality, security, tests. Batches: 4. Raw finding IDs: 1, 2, 3.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/SettingsFragment.java:335](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/SettingsFragment.java:335).

**Assessment / preconditions:** Source inspection confirms the preference-change listener returns true before its asynchronous authentication callback. The threat requires access to an already open settings session; no initial remote authentication bypass was demonstrated.

**Agent-reported impact:** Returning true accepts and persists the switch change immediately, independently of the password callback. Someone with access to an open application session can disable application password protection and cancel or fail the password prompt; the unsuccessful callback does not restore the setting.

**Recommended fix:** Return false and change the persisted switch state only after successful password validation.

**Suggested regression test:** With application password protection enabled, toggle it off and cancel or fail authentication. Assert that the switch and persisted preference remain enabled after reopening settings.

**Exact source excerpt:**

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

### ON-03. [P1] Stored password verifier also serves as the note decryption key

Severity: HIGH (highest agent rating). Status: source_supported_static_assessment. Agents: security. Batches: 3. Raw finding IDs: 9.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:473](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:473).

**Assessment / preconditions:** Source inspection confirms DbHelper decrypts using PREF_PASSWORD. This is a local data-at-rest threat requiring access to preferences and the database, not a demonstrated remote compromise.

**Agent-reported impact:** PasswordHelper verifies passwords against the MD5 value in PREF_PASSWORD, but this stored value is also passed directly to encryption and decryption. An attacker obtaining the preferences and database can decrypt locked notes without recovering the password. Security additionally uses DES, which limits effective key strength to 56 bits.

**Recommended fix:** Use authenticated encryption with a key protected by Android Keystore or derived from the entered password using a salted password KDF. Keep the authentication verifier separate and migrate existing ciphertext.

**Suggested regression test:** Verify that copying the database and password-verifier preferences does not provide sufficient material to decrypt a locked note.

**Exact source excerpt:**

````
          // Eventual decryption of content
          if (Boolean.TRUE.equals(note.isLocked())) {
            note.setContent(
                Security.decrypt(note.getContent(), Prefs.getString(PREF_PASSWORD, "")));
          }
````

### ON-04. [P1] All preferences, including authentication data, are logged

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: security. Batches: 5. Raw finding IDs: 32.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/BaseActivity.java:76](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/BaseActivity.java:76).

**Assessment / preconditions:** Source inspection confirms BaseActivity logs Prefs.getAll(). The visibility and destination of those logs depend on logging configuration, build, and Android storage/access controls.

**Agent-reported impact:** Every activity resume logs all preferences, which include password and recovery-answer entries defined in ConstantsBase. LogDelegate writes these messages to logcat or, when file logging is enabled, to public external storage. An attacker with access to those logs can obtain authentication material; other apps with shared-storage read access can read the public logs on applicable Android versions.

**Recommended fix:** Remove the preference dump. Log only explicitly selected, nonsensitive diagnostic values.

**Suggested regression test:** Populate password and recovery-answer preferences with sentinel values, resume the activity with file logging enabled, and assert neither sentinel appears in captured logs or log files.

**Exact source excerpt:**

````
    LogDelegate.d(Prefs.getAll().toString());
````

### ON-05. [P1] Cryptographic failures silently return unprocessed content

Severity: HIGH (highest agent rating). Status: source_supported_static_assessment. Agents: quality, security, tests. Batches: 1, 2, 3, 4, 5. Raw finding IDs: 14, 15, 16, 17, 18, 19, 82, 83, 84, 85.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:66).

**Assessment / preconditions:** Encryption and decryption catch exceptions and return their input. DbHelper and BackupHelper use the result. The usual password preference contains a long hash; the short-key example requires a missing/corrupt preference or direct invalid input, while provider failures are another possible trigger. The defect is failure reporting, not a claim that all ordinary saves are plaintext.

**Agent-reported impact:** This is fail-open exception handling. Encryption failure returns plaintext as though encryption succeeded, allowing exportNote to write unencrypted content for a locked note. The corresponding decrypt catch also returns its input, so a backup encrypted with another password can be persisted by importNote as ciphertext instead of being rejected.

**Recommended fix:** Return an explicit cryptographic failure or throw a dedicated exception from both operations. Abort the affected export or import before writing content when encryption or decryption fails.

**Suggested regression test:** Force encryption failure and assert that no plaintext backup is written. Import a locked backup with an incorrect password and assert that no note is persisted.

**Exact source excerpt:**

````
            } catch (e: Exception) {
                LogDelegate.e("Something is gone wrong encrypting", e)
                value
            }
````

### ON-06. [P1] Backup encryption truncates the password hash to a weak DES key

Severity: HIGH (highest agent rating). Status: source_supported_static_assessment. Agents: security. Batches: 1, 2, 4, 5. Raw finding IDs: 12, 13, 80, 81.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:58](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/Security.kt:58).

**Assessment / preconditions:** DES use and first-eight-byte key handling are visible in source. A hexadecimal password verifier is used at call sites. Do not interpret this static result as a successful brute-force attack or a measured attack cost.

**Agent-reported impact:** BackupHelper.exportNote passes PREF_PASSWORD into this function, and PasswordActivity stores that value as hexadecimal MD5. DESKeySpec uses only the first eight bytes, so the encryption key has at most 32 bits of input entropy from eight hexadecimal characters, further reduced by DES parity bits. An attacker who obtains a locked-note backup can brute-force this small key space offline regardless of the original password's strength.

**Recommended fix:** Use authenticated encryption such as AES-GCM with a random nonce and a properly salted password derivation function. Version the backup format and retain legacy decryption only for migration.

**Suggested regression test:** Verify that two password inputs sharing their first eight characters cannot decrypt each other's new-format ciphertext, repeated encryption produces different ciphertext, and modified ciphertext is rejected.

**Exact source excerpt:**

````
                val keySpec = DESKeySpec(password.toByteArray(StandardCharsets.UTF_8))
                val keyFactory = SecretKeyFactory.getInstance("DES")
                val key = keyFactory.generateSecret(keySpec)
                val clearText = value.toByteArray(StandardCharsets.UTF_8)
                // Cipher is not thread safe
                val cipher = Cipher.getInstance("DES")
````

### ON-07. [P1] Duplicate-creation migration can preserve duplicates and update multiple notes

Severity: HIGH (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 2. Raw finding IDs: 4.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/async/upgrade/UpgradeProcessor.java:171](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/async/upgrade/UpgradeProcessor.java:171).

**Assessment / preconditions:** The update predicate is not a unique row identifier and can change several duplicate rows together. This should be tested with legacy databases before modifying released migration logic.

**Agent-reported impact:** Two notes sharing creation, title, and content both match this UPDATE and receive the same new creation value, so they remain duplicates. Even for distinct content, the random offset can be zero or collide with another creation. This fails the migration's uniqueness requirement before creation becomes the primary key, potentially preventing the transition.

**Recommended fix:** Update each row by its existing unique ID and allocate a deterministic unused creation value, tracking newly assigned values.

**Suggested regression test:** Migrate two identical notes with the same creation plus nearby occupied timestamps; assert that every row survives and all resulting creation values are unique.

**Exact source excerpt:**

````
        ContentValues values = new ContentValues();
        values.put(DbHelper.KEY_CREATION, note.getCreation() + (long) (Math.random() * 999));
        DbHelper.getInstance().getDatabase()
            .update(DbHelper.TABLE_NOTES, values, DbHelper.KEY_TITLE +
                    " = ? AND " + DbHelper.KEY_CREATION + " = ? AND " + DbHelper.KEY_CONTENT + " = ?",
                new String[]{note
                    .getTitle(), String.valueOf(note.getCreation()), note.getContent()});
````

### ON-08. [P1] Millisecond attachment IDs can overwrite other attachments

Severity: HIGH (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 3. Raw finding IDs: 8.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:306](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:306).

**Assessment / preconditions:** Source inspection confirms millisecond-derived IDs with CONFLICT_REPLACE. Collision risk requires multiple inserts with matching timestamps; no on-device collision was reproduced.

**Agent-reported impact:** Two new attachments saved in the same millisecond receive the same primary key. The CONFLICT_REPLACE insertion at line 314 then deletes the earlier attachment row. The generated ID is also never assigned back to the attachment, so saving the same new object again can insert another row.

**Recommended fix:** Let SQLite generate IDs for new attachments, capture the inserted row ID, and assign it to the attachment. Preserve explicit IDs only for existing rows.

**Suggested regression test:** Save multiple attachments with a fixed clock, then save them again; assert every attachment has a distinct persisted ID and the row count remains unchanged on the second save.

**Exact source excerpt:**

````
    valuesAttachments.put(KEY_ATTACHMENT_ID,
        attachment.getId() != null ? attachment.getId() : Calendar.getInstance().getTimeInMillis());
````

### ON-09. [P1] Note updates leave transactions open when an operation throws

Severity: HIGH (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 3. Raw finding IDs: 5.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:266](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:266).

**Assessment / preconditions:** Source inspection confirms beginTransaction/endTransaction are not paired with finally. Exceptions during the intervening work can skip cleanup.

**Agent-reported impact:** The transaction begun at line 227 has no finally cleanup. An exception during attachment processing, such as dereferencing a null attachment URI at line 309, skips endTransaction(), retaining the transaction and potentially blocking subsequent database operations.

**Recommended fix:** Wrap the transaction body in try/finally, mark success only after all writes succeed, and always call endTransaction() in finally.

**Suggested regression test:** Force an attachment write to throw; assert the note update rolls back and another thread can subsequently write to the database.

**Exact source excerpt:**

````
    db.setTransactionSuccessful();
    db.endTransaction();
````

### ON-10. [P1] Persistable folder permission flags always evaluate to zero

Severity: HIGH (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 4. Raw finding IDs: 10, 68.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:273](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:273).

**Assessment / preconditions:** Source inspection confirms READ & WRITE evaluates to zero. Correct the grant mask using the actual granted intent flags. The precise exception/provider behavior requires Android instrumentation; do not limit the regression to reboot only.

**Agent-reported impact:** Read and write permission flags are distinct bits, so their bitwise AND is zero. The selected backup folder therefore receives no persisted read or write grant, leaving later backup operations without access once the temporary grant expires.

**Recommended fix:** Mask intent.getFlags() with the bitwise OR of the read and write flags, and persist the granted permissions.

**Suggested regression test:** Select a backup folder, restart the device, and assert that its persisted URI permission includes read and write access and a backup can complete.

**Exact source excerpt:**

````
    final int takeFlags = FLAG_GRANT_READ_URI_PERMISSION & FLAG_GRANT_WRITE_URI_PERMISSION;
    context.getContentResolver().takePersistableUriPermission(intent.getData(), takeFlags);
````

### ON-11. [P2] Widget fill-in intents expose decrypted locked notes to the host

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: security. Batches: 3. Raw finding IDs: 91.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/widget/ListRemoteViewsFactory.java:127](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/widget/ListRemoteViewsFactory.java:127).

**Assessment / preconditions:** This depends on locked notes being returned to a widget and a host able to inspect RemoteViews. Source inspection confirms full Note parceling, but no malicious host extraction was executed.

**Agent-reported impact:** DbHelper.getNotes decrypts locked content before returning notes. This code embeds the entire note in RemoteViews delivered to the widget host, and Note.writeToParcel includes its content. If a locked note is included in the widget query, a malicious widget host can inspect its plaintext even when the displayed text is masked.

**Recommended fix:** Put only the note identifier in widget fill-in intents. Retrieve the note inside the app and require authentication before exposing locked content.

**Suggested regression test:** Include a locked note in a widget and inspect the delivered RemoteViews intent extras; assert that neither plaintext content nor the full Note parcel is present.

### ON-12. [P2] Attachments belonging to locked notes are exported without encryption

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: security. Batches: 4. Raw finding IDs: 65.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:140](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:140).

**Assessment / preconditions:** The backup attachment copy is plaintext. Whether users expect attachment encryption alongside locked text should be documented; the report does not claim all app storage is encrypted.

**Agent-reported impact:** exportAttachments obtains all database attachments and copies their original bytes into the backup directory without checking note protection. Although exportNote encrypts locked-note content, its images, recordings, and other attachments remain readable to anyone who obtains access to the backup folder or its storage provider.

**Recommended fix:** Encrypt attachments associated with protected notes using authenticated encryption, and record the encryption metadata needed for restoration.

**Suggested regression test:** Export a locked note with an attachment containing a known marker. Assert that the backup attachment does not expose the original bytes and can be restored only with the correct secret.

### ON-13. [P2] Note export failures are swallowed

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 4. Raw finding IDs: 64.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:78](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:78).

**Agent-reported impact:** This is the swallowed-exception anti-pattern. If storage fills or the provider fails while writing a note, exportNote returns normally and exportNotes continues without any failure result. Callers cannot distinguish a complete backup from one missing note contents.

**Recommended fix:** Propagate the write failure or return an explicit result that exportNotes aggregates and reports as an incomplete backup.

**Suggested regression test:** Make a note write throw IOException and assert that the overall export reports failure and identifies the affected note.

### ON-14. [P2] Unreadable backup notes become empty notes during import

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 4. Raw finding IDs: 66.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:187](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:187).

**Agent-reported impact:** This is the error-as-success-value anti-pattern. An unreadable JSON file produces a non-null empty Note, which passes importNotes' non-null filter and reaches updateNote in importNote. An empty file likewise returns the newly constructed Note. Failed reads are consequently treated as successful note imports.

**Recommended fix:** Reject empty content and propagate a descriptive import failure, or return null and explicitly report skipped files before any database update.

**Suggested regression test:** Import an empty file and a file whose read throws IOException. Assert that neither creates a database note and both are reported as failed.

### ON-15. [P2] Missing attachment directory crashes restore

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 4. Raw finding IDs: 67.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:199](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/BackupHelper.java:199).

**Agent-reported impact:** findFile can return null when the backup contains no attachment directory, such as an incomplete or manually copied backup. Calling exists on that result throws NullPointerException instead of returning the intended failure result.

**Recommended fix:** Check for null and verify that the entry is a directory before accessing its contents.

**Suggested regression test:** Restore from a backup without an attachment directory and assert that importAttachments returns false without throwing.

### ON-16. [P2] The address migration discards every note's trash status

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 1. Raw finding IDs: 29, 30.

Location: [omniNotes/src/main/assets/sql/upgrade-453.sql:23](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/assets/sql/upgrade-453.sql:23).

**Agent-reported impact:** The replacement table declares trashed, but the copy omits it. Migrated rows receive NULL instead of their existing trash status, and dropping notes_tmp permanently loses that state. The supplied reminder tests create fresh rows and cannot detect migration damage.

**Recommended fix:** Include trashed in both the INSERT and SELECT column lists.

**Suggested regression test:** Seed the pre-migration table with trashed=1 and trashed=0 notes, run upgrade-453.sql, and assert both values and all existing note fields are preserved.

### ON-17. [P2] Reminder migration compares milliseconds against seconds

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 2. Raw finding IDs: 31.

Location: [omniNotes/src/main/assets/sql/upgrade-482.sql:31](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/assets/sql/upgrade-482.sql:31).

**Agent-reported impact:** The supplied reminder tests store alarm timestamps in milliseconds, whereas strftime('%s', 'now') returns seconds. Adding 1000 does not convert units. Ordinary past reminders therefore fail this predicate and are not marked fired during migration.

**Recommended fix:** Multiply the Unix timestamp by 1000 before comparing it with alarm.

**Suggested regression test:** Migrate notes with alarms one minute before and after the current time; assert that only the past alarm is marked fired.

### ON-18. [P2] Tag search interpolates input into executable SQL

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, security, tests. Batches: 3. Raw finding IDs: 58, 59, 60.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:763](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:763).

**Assessment / preconditions:** Treat SQL construction with untrusted text as a code defect. Reachability and exploitability depend on allowed tag inputs and call sites; no extraction, arbitrary statement execution, or remote attack was demonstrated.

**Agent-reported impact:** Tag values are inserted into SQL string literals without escaping or binding, and getNotes executes the resulting query with rawQuery. If an attacker can influence a searched tag, an apostrophe can cause an uncaught SQL error, while crafted SQL can alter the selection. The later regex filter runs only after SQL execution and cannot prevent injection.

**Recommended fix:** Bind tag patterns through selection arguments, escaping LIKE metacharacters when literal matching is intended.

**Suggested regression test:** Search for tags containing apostrophes and SQL syntax; assert that they are treated literally, do not throw, and do not broaden the SQL selection.

### ON-19. [P2] Single-line SQL comments consume subsequent statements

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 5. Raw finding IDs: 61, 62.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/db/SqlParser.java:63](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/SqlParser.java:63).

**Agent-reported impact:** The block-comment opener checks for a closing brace instead of */. A complete comment such as /* migration */ enters multiline-comment mode, and all following SQL is discarded until another line ends in */. A script can therefore silently omit its migration statements.

**Recommended fix:** Recognize a closing */ on the opening line, preferably using a parser that tracks comment delimiters and preserves SQL outside them.

**Suggested regression test:** Parse '/* migration */\nCREATE TABLE example(id INTEGER);' and assert that the CREATE TABLE statement is returned.

### ON-20. [P2] Attachment copy failures are reported as success

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 5. Raw finding IDs: 86, 87.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:127](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:127).

**Agent-reported impact:** The copyFile overload catches IOException and returns false, but this caller ignores that result. A read failure or full storage therefore returns a partial file as a valid attachment, and the surrounding IOException fallback never runs for the copy failure.

**Recommended fix:** Check the result or use a throwing copy operation. Delete partial output and return failure before constructing an Attachment.

**Suggested regression test:** Use an input stream that throws after several bytes; assert that attachment creation fails and leaves no partial attachment file.

### ON-21. [P2] Attachment names can collide within the same millisecond

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 5. Raw finding IDs: 88.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:248](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:248).

**Agent-reported impact:** Synchronization serializes calls but does not make timestamps unique. Two attachments with the same extension created within one millisecond receive the same path. FileOutputStream then truncates the earlier attachment, so both notes can reference the later file.

**Recommended fix:** Reserve unique files atomically with File.createTempFile or use collision-resistant names with exclusive creation.

**Suggested regression test:** Create multiple attachment files with a fixed clock and identical extensions; assert distinct paths and preserved contents.

### ON-22. [P2] Backup copying leaks its output stream and hides failure

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 5. Raw finding IDs: 89.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:272](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/StorageHelper.java:272).

**Agent-reported impact:** This resource-leak pattern opens a FileOutputStream that neither this method nor copyFile closes. Repeated backup copies can exhaust file descriptors. The ignored copy result and unconditional destination return also present incomplete or nonexistent backups as successful.

**Recommended fix:** Own the output stream with try-with-resources and propagate copy/open failures or return an explicit failure after deleting partial output.

**Suggested regression test:** Force a copy IOException and assert failure rather than a destination result; verify the output stream closes on success and failure.

### ON-23. [P2] Queued alarms can overwrite a trashed note with stale data

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: tests. Batches: 1. Raw finding IDs: 76.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/receiver/AlarmReceiver.java:55](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/receiver/AlarmReceiver.java:55).

**Agent-reported impact:** The guard only checks existence. A queued broadcast serialized before trashing still passes because the database row exists, then displays a notification and writes its old, untrashed state through updateNote(). The supplied receiver test covers deletion only, so it misses this path and stale edits to existing notes.

**Recommended fix:** Load the current database note, reject trashed notes and obsolete alarms, and apply reminder changes to current data.

**Suggested regression test:** Serialize an active reminded note, trash and save it, then deliver the original broadcast. Assert the database note remains trashed, no notification appears, and no recurrent alarm is scheduled. Also edit the title after serialization and assert delivery preserves the edit.

### ON-24. [P2] Denied exact-alarm access launches settings from an application context

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 1. Raw finding IDs: 78, 79.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/utils/ReminderHelper.java:63](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/ReminderHelper.java:63).

**Agent-reported impact:** SaveNoteTask supplies OmniNotes.getAppContext(). When exact-alarm access is denied on Android 12+, startActivity() lacks FLAG_ACTIVITY_NEW_TASK and throws from that application context. The reminder tests assume scheduling succeeds and do not exercise denied access.

**Recommended fix:** Handle permission requests through an activity, or add the required task flag when launching from an application context and provide a way to retry scheduling after access is granted.

**Suggested regression test:** On API 31+, simulate canScheduleExactAlarms() returning false and call addReminder with an application context. Assert no exception, the settings intent has FLAG_ACTIVITY_NEW_TASK, and no alarm is scheduled before permission is granted.

### ON-25. [P2] Postponing a recurring reminder skips the selected occurrence

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 5. Raw finding IDs: 54.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/SnoozeActivity.java:137](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/SnoozeActivity.java:137).

**Agent-reported impact:** ReminderPickers first calls onReminderPicked, which sets the alarm to the selected future time. This callback then calls setNextRecurrentReminder, whose helper searches after that alarm plus one minute. Selecting tomorrow at 09:00 with daily recurrence consequently saves the following day's 09:00 instead.

**Recommended fix:** Save the selected alarm and recurrence directly when confirming the picker. Advance recurrence only when dismissing or completing a fired reminder.

**Suggested regression test:** Postpone a daily reminder to tomorrow at 09:00 and assert that the saved alarm is tomorrow at 09:00.

### ON-26. [P2] Today's reminders are selected using UTC dates

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 3. Raw finding IDs: 57.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:653](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/db/DbHelper.java:653).

**Agent-reported impact:** SQLite evaluates both dates in UTC. In a non-UTC timezone, reminders near midnight can fall on a different local day, so getTodayReminders omits reminders due today and includes reminders due yesterday or tomorrow.

**Recommended fix:** Compute the local day's start and next day's start in the application timezone and query the timestamp interval.

**Suggested regression test:** In Australia/Melbourne, query reminders around local midnight and assert only timestamps within the current local calendar day are returned.

### ON-27. [P2] Tomorrow reminders are classified by elapsed hours instead of calendar date

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 4. Raw finding IDs: 63.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/extensions/ONDashClockExtension.java:133](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/extensions/ONDashClockExtension.java:133).

**Agent-reported impact:** At 08:00 today, a reminder at 20:00 tomorrow is excluded because it is 36 hours away. Conversely, an unfired reminder from yesterday has a negative difference and is labeled tomorrow. Elapsed hours do not identify the next calendar day.

**Recommended fix:** Compare the alarm's local calendar date with a Calendar advanced by one day, using a single captured current time.

**Suggested regression test:** Assert that tomorrow evening is included when now is this morning, yesterday is excluded, and classification remains correct across daylight-saving transitions.

### ON-28. [P2] Activity stops receiving events after its first stop

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 5. Raw finding IDs: 46, 47.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:162](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:162).

**Agent-reported impact:** Registration occurs only in onCreate, whereas onStop unregisters the activity. Returning to the same activity instance does not call onCreate, leaving its PasswordRemovedEvent and NotificationsGrantedEvent handlers disconnected. The supplied UI tests do not exercise this stop/start transition.

**Recommended fix:** Pair registration and unregistration in matching lifecycle callbacks, such as onStart and onStop.

**Suggested regression test:** Launch MainActivity, move it through stopped and started states without recreating it, and assert that it is registered and handles a posted NotificationsGrantedEvent after returning.

### ON-29. [P2] Malformed VIEW intents crash the activity

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 5. Raw finding IDs: 48.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:439](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:439).

**Agent-reported impact:** An ACTION_VIEW intent without data dereferences null here. With data present, the subsequent shortcut branch also parses an absent or nonnumeric id without handling NumberFormatException. MainActivity is exported, so either malformed input can terminate it.

**Recommended fix:** Validate the URI, scheme, host, and numeric ID before dispatching; reject malformed input without throwing.

**Suggested regression test:** Deliver ACTION_VIEW with no data, an app URI without id, and id=abc; assert that none crashes or opens an unintended note.

### ON-30. [P2] Sharing multiple missing attachments crashes

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 5. Raw finding IDs: 49, 50.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:563](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/MainActivity.java:563).

**Agent-reported impact:** getShareableAttachmentUri returns null for missing files, and those entries are skipped. If all attachments are missing, mimeTypes is empty and indexing element zero throws instead of handling the failure.

**Recommended fix:** Handle an empty set of shareable attachments explicitly before selecting a MIME type or launching the chooser.

**Suggested regression test:** Share a note containing two attachments whose files are absent. Assert no exception and either a documented text-only share or an error with no chooser launch. Also test one missing and one valid attachment.

### ON-31. [P2] Sketch save errors discard the drawing without informing the user

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 5. Raw finding IDs: 53.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/SketchFragment.java:206](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/SketchFragment.java:206).

**Agent-reported impact:** This swallowed-exception pattern makes save return normally when opening or writing the file fails. MainActivity.handleBackPressed unconditionally pops the sketch immediately after save(), so a storage failure closes the editor and loses the user's drawing without a visible error.

**Recommended fix:** Return a save result or propagate a specific failure, show an error, and navigate away only after confirmed successful writing. Check Bitmap.compress's result as well.

**Suggested regression test:** Use an unwritable output path, press Back, and assert that an error appears and the sketch remains available for retry.

### ON-32. [P2] Recording failures leave a recorder that Stop cannot safely stop

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 1. Raw finding IDs: 38.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:1833](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:1833).

**Agent-reported impact:** This is incomplete error recovery: isRecording is set before preparation, but this catch neither resets it nor releases mRecorder. If prepare fails, the next recording-button click calls stopRecording, whose unguarded mRecorder.stop() throws because recording never started. Stopping immediately after a successful start can also throw when insufficient audio has been captured.

**Recommended fix:** Set isRecording only after start succeeds, release and clear the recorder on failure, and handle stop failures with cleanup in a finally block. Attach a recording only after a successful stop.

**Suggested regression test:** Simulate prepare throwing IOException, then click the recording control again; assert no crash, a released recorder, and no invalid attachment.

### ON-33. [P2] Completed playback abandons the MediaPlayer without releasing it

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 1. Raw finding IDs: 37.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:1782](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:1782).

**Agent-reported impact:** This is a resource leak. Each naturally completed playback clears the only field used by stopPlaying to release the player, without releasing mp. Repeatedly playing attachments accumulates native media resources until garbage collection and can exhaust playback resources.

**Recommended fix:** Release mp in the completion callback before clearing the field, and release the player on preparation failures as well.

**Suggested regression test:** Complete playback repeatedly with a mocked MediaPlayer; assert release is called exactly once for every created player.

### ON-34. [P2] Process Text reads a CharSequence extra as a String

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 1. Raw finding IDs: 34.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:532](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:532).

**Agent-reported impact:** EXTRA_PROCESS_TEXT carries a CharSequence, which can be a styled text object rather than a String. getStringExtra can return null for that valid payload, and the immediate toString call then crashes the activity. A missing extra also crashes.

**Recommended fix:** Read the value with getCharSequenceExtra and convert it to a String only after checking for null.

**Suggested regression test:** Launch ACTION_PROCESS_TEXT with a SpannableString payload and assert that its text becomes the note content without a crash.

### ON-35. [P2] Downloads URI parsing assumes document IDs are numeric

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 2. Raw finding IDs: 77.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/utils/FileHelper.java:67](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/utils/FileHelper.java:67).

**Agent-reported impact:** Downloads document IDs can contain prefixes such as raw: or msf:. Passing such a valid document URI to getPath throws NumberFormatException before reaching getDataColumn's error handling, interrupting file selection.

**Recommended fix:** Handle supported document-ID forms explicitly and use ContentResolver streams when a document has no usable filesystem path.

**Suggested regression test:** Pass Downloads document URIs with numeric, raw:, and msf: IDs; assert that supported forms resolve and unsupported forms return a controlled result without throwing.

### ON-36. [P2] Gallery initialization indexes an explicitly permitted empty list

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: tests. Batches: 3. Raw finding IDs: 40.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/GalleryActivity.java:163](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/GalleryActivity.java:163).

**Agent-reported impact:** initData defaults missing GALLERY_IMAGES to Collections.emptyList(), then unconditionally indexes it here. Missing or empty images therefore crash initialization. Negative or out-of-range GALLERY_CLICKED_IMAGE values also crash, even if ViewPager clamps its own current item.

**Recommended fix:** Handle empty images before configuring the gallery and validate the requested index before accessing the list.

**Suggested regression test:** Launch GalleryActivity with missing images, an empty image list, and a single image with indices -1 and 1. Assert graceful completion or a defined fallback without IndexOutOfBoundsException.

### ON-37. [P2] Opening media crashes when no viewer is installed

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 3. Raw finding IDs: 41.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/GalleryActivity.java:190](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/GalleryActivity.java:190).

**Agent-reported impact:** A device without an activity supporting the attachment's MIME type throws ActivityNotFoundException. Videos invoke this path automatically during gallery initialization, so simply opening such a video crashes the gallery.

**Recommended fix:** Catch ActivityNotFoundException and display a clear message while keeping the gallery usable.

**Suggested regression test:** Open a video with no matching external viewer installed; assert the gallery remains open and reports that no viewer is available.

### ON-38. [P2] Temporary category navigation can crash new-note creation

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 2. Raw finding IDs: 42.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:938](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:938).

**Agent-reported impact:** Java evaluates both arguments before calling defaultIfNull. When a widget supplies navigationTmp while the persistent navigation has no category, Navigation.getCategory().toString() can throw NullPointerException even though the temporary category is available. The surrounding catch handles only NumberFormatException.

**Recommended fix:** Select the category ID with a conditional expression so Navigation.getCategory() is evaluated only when needed, and handle an absent category.

**Suggested regression test:** Open a category widget while persistent navigation is Notes, then create a note; assert that creation succeeds with the widget category.

### ON-39. [P2] Activity weak reference is dereferenced before the lifecycle guard

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 3. Raw finding IDs: 55, 56.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/async/MainMenuTask.java:61](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/async/MainMenuTask.java:61).

**Agent-reported impact:** If the activity is destroyed and collected while the background task runs, mainActivity.get() returns null and onPostExecute crashes before reaching isAlive().

**Recommended fix:** Resolve weak references once into local variables, validate the activity and fragment lifecycle first, and only then access the drawer.

**Suggested regression test:** Destroy the hosting activity before task completion and clear its weak reference; assert completion exits without accessing views or throwing.

### ON-40. [P2] Asynchronous deletion events refresh drawer views on a worker thread

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 4. Raw finding IDs: 51.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/NavigationDrawerFragment.java:150](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/NavigationDrawerFragment.java:150).

**Agent-reported impact:** EventBus runs onEventAsync on a background thread. refreshMenus calls mDrawerToggle.syncState and executes CategoryMenuTask, whose onPreExecute immediately accesses drawer views and can add a footer. These UI operations therefore run off the main thread during note deletion, risking thread violations and inconsistent drawer updates.

**Recommended fix:** Handle this event with onEventMainThread, keeping database work inside the tasks' background phases.

**Suggested regression test:** Post NotesDeletedEvent and assert that drawer synchronization and CategoryMenuTask.onPreExecute execute on the main looper.

### ON-41. [P2] Note updates always skip the final list item

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 2. Raw finding IDs: 43, 44.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:1190](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:1190).

**Agent-reported impact:** IntStream.range excludes its upper bound, so the final note is never updated. With one note, no items are examined. NoteLocationTest posts a CategoriesUpdatedEvent after NotesUpdatedEvent, causing a full reload that masks this defect.

**Recommended fix:** Use the list size as the exclusive upper bound and test NotesUpdatedEvent without a subsequent full reload.

**Suggested regression test:** Load a single note, post only NotesUpdatedEvent with changed title and location, and assert the adapter and displayed row contain the new values. Repeat for the last item of a multi-note list.

### ON-42. [P2] Undoing trash does not restore the canceled reminder

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 2. Raw finding IDs: 45.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:1304](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/ListFragment.java:1304).

**Agent-reported impact:** Trashing cancels reminders before the operation is committed. onUndo restores adapter items and clears the pending state without rescheduling their reminders. Trashing a note with a future reminder and pressing Undo therefore leaves the note active but its alarm canceled.

**Recommended fix:** Defer reminder cancellation until trash is committed, or explicitly reschedule reminders when undoing trash.

**Suggested regression test:** Schedule a future reminder, trash the note, and undo; assert that the note remains active and its reminder is still scheduled.

### ON-43. [P2] Removing all attachments disconnects the adapter from subsequent additions

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 1. Raw finding IDs: 39.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:2018](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:2018).

**Agent-reported impact:** The note and adapter receive different empty lists. Subsequent attachment callbacks add to noteTmp and notify the adapter, but the adapter still observes its separate empty list. Attachments added after Delete All therefore do not appear in the grid.

**Recommended fix:** Construct the replacement adapter with noteTmp.getAttachmentsList(), as initViewAttachments does.

**Suggested regression test:** Delete all attachments, then add another attachment; assert that the grid displays the new attachment and the note contains it.

### ON-44. [P2] Changing a note's coordinates retains its previous address

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 1. Raw finding IDs: 35, 36.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:940](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/DetailFragment.java:940).

**Agent-reported impact:** When a note already has an address and the user retrieves a different location, the coordinates change but the old address suppresses reverse geocoding. The note displays and retains the old place while opening the map at the new place. Removing a location also leaves the address intact, so adding another location reproduces this mismatch.

**Recommended fix:** Invalidate the cached address when coordinates change or are removed, then resolve the address for the new coordinates.

**Suggested regression test:** Start with coordinates and address A, retrieve location B, and assert that address A is cleared and replaced by B's address or coordinates.

### ON-45. [P2] Location cache selection ignores how old the fix is

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 1. Raw finding IDs: 69, 70.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/helpers/location/LocationManagerLocationProvider.java:118](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/location/LocationManagerLocationProvider.java:118).

**Agent-reported impact:** The provider selects cached fixes solely by accuracy and getLocation immediately returns the selected fix without requesting an update. An accurate GPS fix from a previous trip therefore beats a recent network fix and can be attached to a new note as the device's current position.

**Recommended fix:** Reject fixes older than a defined freshness threshold using elapsed realtime, consider recency when comparing fixes, and request an update when no sufficiently fresh fix exists.

**Suggested regression test:** Provide an old accurate GPS fix and a recent network fix; assert that the old fix is not returned as the current position.

### ON-46. [P2] Notification cancellation does not match the identity used by show

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 3. Raw finding IDs: 71, 72.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/helpers/notifications/NotificationsHelper.java:207](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/helpers/notifications/NotificationsHelper.java:207).

**Agent-reported impact:** show(long) posts notifications with a string tag and numeric ID 0, but cancel(int) and cancel() use the untagged cancellation overload. Consequently, show(42) followed by cancel(42), or show() followed by cancel(), leaves the posted notification active.

**Recommended fix:** Use consistent tag and ID pairs for posting and cancellation, while preserving the separate untagged progress notification behavior if needed.

**Suggested regression test:** Post with show(42), cancel that notification, and assert its tagged entry is absent from active notifications. Repeat with show() and cancel(), and verify cancellation leaves an unrelated notification intact.

### ON-47. [P2] Empty-state observer ignores granular insertions and removals

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 2. Raw finding IDs: 74, 75.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/models/views/RecyclerViewEmptySupport.java:32](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/models/views/RecyclerViewEmptySupport.java:32).

**Agent-reported impact:** The observer implements only onChanged. RecyclerView notifications such as notifyItemRemoved and notifyItemInserted invoke separate callbacks, so removing the last item or inserting the first item through these notifications leaves the empty-state visibility stale. Existing lifecycle tests largely exercise paths that explicitly call notifyDataSetChanged.

**Recommended fix:** Recalculate empty-state visibility from range insertion and removal callbacks as well as onChanged.

**Suggested regression test:** Attach an adapter containing one item, remove it and call only notifyItemRemoved(0); assert the empty view is visible and the list is gone. Insert the first item with only notifyItemInserted(0) and assert the inverse.

### ON-48. [P2] Category color selection is lost on activity recreation

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 2. Raw finding IDs: 33.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/CategoryActivity.java:82](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/CategoryActivity.java:82).

**Agent-reported impact:** onColorSelection updates selectedColor but does not update category. Only category is saved, and onCreate restores selectedColor from category.getColor(). Rotating after choosing a color therefore discards that choice, and saving persists the old color.

**Recommended fix:** Save and restore selectedColor explicitly or update the category's color when the selection changes.

**Suggested regression test:** Choose a different category color, recreate the activity, and save; assert that the chosen color remains displayed and is persisted.

### ON-49. [P2] Settings recreation overwrites restored navigation

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 4. Raw finding IDs: 52.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/SettingsActivity.java:64](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/SettingsActivity.java:64).

**Agent-reported impact:** After rotation or process recreation, FragmentManager restores the current settings fragment and its back stack. This unconditional replacement overwrites that restored screen with the root settings fragment while leaving the restored back stack in place, losing the user's location and making subsequent back navigation inconsistent.

**Recommended fix:** Install the initial SettingsFragment only when savedInstanceState is null and otherwise retain FragmentManager's restored state.

**Suggested regression test:** Open a nested settings screen, recreate the activity, and assert that the same screen remains visible and Back returns to its parent.

### ON-50. [P2] Widget display preferences are shared globally and lost on restart

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 3. Raw finding IDs: 90.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/widget/ListRemoteViewsFactory.java:65](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/widget/ListRemoteViewsFactory.java:65).

**Agent-reported impact:** This is hidden shared mutable state: thumbnail and timestamp settings are static fields used by every widget, while only the SQL condition is persisted per widget. Configuring a second widget changes the first widget's display, and process restart resets both settings to true.

**Recommended fix:** Persist both display settings under widget-specific keys and load them into instance fields for each factory.

**Suggested regression test:** Configure two widgets with opposite display settings, recreate their factories, and assert each retains its own settings.

### ON-51. [P2] DashClock and Pushbullet cannot bind to their extension services

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 2, 4. Raw finding IDs: 27, 28.

Location: [omniNotes/src/main/AndroidManifest.xml:287](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/AndroidManifest.xml:287).

**Assessment / preconditions:** Both declarations are exported=false. Restoring third-party integrations requires reviewing intended bindings and permission protection; do not simply export services without that assessment.

**Agent-reported impact:** DashClock runs under another application's UID and cannot bind to a service marked exported=false, even with the declared permission. PushBulletExtension has the same configuration at lines 308–311, preventing that integration as well.

**Recommended fix:** Export the extension services intended for external applications while retaining their permission restrictions.

**Suggested regression test:** From clients holding the respective extension permissions, assert that both services can be discovered and bound.

### ON-52. [P3] Retry loop exits before the timeout

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 5. Raw finding IDs: 21, 22.

Location: [omniNotes/src/androidTest/java/it/feio/android/omninotes/testutils/RetryableAssert.java:54](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/testutils/RetryableAssert.java:54).

**Agent-reported impact:** The loop repeats only when the clock exactly equals the deadline. For a normal positive timeout it exits immediately, so asynchronous assertions fail before their allowed waiting period.

**Recommended fix:** Retry while the deadline has not passed, return on success, and fail only after the timeout.

**Suggested regression test:** Use a predicate that becomes true after 100 ms with a 1000 ms timeout and assert success. Also verify that an always-false predicate fails after the allowed interval.

### ON-53. [P3] Camera assertions cannot both succeed and may never run

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 5. Raw finding IDs: 23, 24.

Location: [omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/FabCameraNoteTest.java:93](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/FabCameraNoteTest.java:93).

**Agent-reported impact:** An empty attachment list cannot have element zero. Furthermore, these assertions exist only in an EventBus callback; the test body never asserts that the callback occurred or waits for its result. Missing events can therefore leave the camera behavior unverified.

**Recommended fix:** Capture the event, await it with a bounded synchronization mechanism, and assert the expected attachment count and MIME type on the test thread. Release Intents and unregister the subscriber in teardown.

**Suggested regression test:** Complete the stubbed camera capture and assert that an update arrives and contains exactly one image attachment. Suppress the update in a negative scenario and verify that the test fails on timeout.

### ON-54. [P3] FAB action assertions never resolve the matched views

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: quality, tests. Batches: 4. Raw finding IDs: 25, 93.

Location: [omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/FabLifecycleTest.java:69](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/FabLifecycleTest.java:69).

**Agent-reported impact:** Espresso onView returns a ViewInteraction without resolving the matcher. Checking that interaction for null therefore passes even when the checklist action is missing or hidden. The camera assertion has the same problem, so fabActionsTest does not verify either action's visibility.

**Recommended fix:** Execute check(matches(isDisplayed())) on both interactions and verify collapse hides the actions.

**Suggested regression test:** Expand the FAB and assert checklist and camera views are displayed using Espresso checks. Collapse it and assert they are not displayed. Verify the expanded-state assertion fails if either action is hidden.

### ON-55. [P3] Create-note UI test never verifies that the note was saved

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: tests. Batches: 2. Raw finding IDs: 26.

Location: [omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/NoteLifecycleTest.java:74](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/ui/NoteLifecycleTest.java:74).

**Agent-reported impact:** The test ends after navigation without asserting any saved state. A regression that silently discards the title, content, or entire note can pass as long as the editing controls and navigation still work.

**Recommended fix:** Assert the resulting note appears in the list and retains its values when reopened.

**Suggested regression test:** Create a note with title "Note title" and content "Note content", navigate up, assert exactly one saved note with those values, then reopen it and assert both editor fields.

### ON-56. [P3] Upgrade assertion also passes if migration deletes attachments

Severity: MEDIUM (highest agent rating). Status: source_supported_static_assessment. Agents: tests. Batches: 5. Raw finding IDs: 20.

Location: [omniNotes/src/androidTest/java/it/feio/android/omninotes/async/upgrade/UpgradeProcessorTest.kt:41](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/async/upgrade/UpgradeProcessorTest.kt:41).

**Agent-reported impact:** allMatch returns true for an empty collection. The test therefore accepts loss of every attachment, and it does not establish that the migrated URI still points to the original data needed for backups.

**Recommended fix:** Assert preservation of the note and attachment identities and count, then read the migrated attachment and compare its contents.

**Suggested regression test:** Seed one content URI attachment with known bytes, migrate, reload its note, and assert exactly one attachment remains with the original identity, a usable file URI, and identical bytes.

### ON-57. [P3] Exception wrapper discards the original cause

Severity: LOW (highest agent rating). Status: source_supported_static_assessment. Agents: quality. Batches: 5. Raw finding IDs: 92.

Location: [omniNotes/src/androidTest/java/it/feio/android/omninotes/exceptions/TestException.java:26](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/exceptions/TestException.java:26).

**Agent-reported impact:** This lost-cause exception-wrapping pattern ignores the supplied exception. A wrapped setup or I/O failure loses its message and original stack trace, obscuring the reason the test failed.

**Recommended fix:** Call super(e) or super(message, e) to preserve the cause.

**Suggested regression test:** Construct TestException with an IOException and assert that getCause() returns that same exception.

### ON-58. [P3] Google Play availability assertion cannot detect an incorrect result

Severity: LOW (highest agent rating). Status: source_supported_static_assessment. Agents: tests. Batches: 1. Raw finding IDs: 94.

Location: [omniNotes/src/androidTest/java/it/feio/android/omninotes/utils/MiscUtilsTest.kt:29](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/androidTest/java/it/feio/android/omninotes/utils/MiscUtilsTest.kt:29).

**Agent-reported impact:** Checking the result's Boolean type does not verify availability behavior. An implementation that always returns true or always returns false can pass this test.

**Recommended fix:** Control the availability dependency and assert the expected Boolean value for each relevant state.

**Suggested regression test:** Arrange Google Play services as available and assert true; arrange services as missing or unavailable and assert false.

### ON-59. [P3] Comma-tag test supplies an invalid selection and checks unchanged input

Severity: LOW (highest agent rating). Status: source_supported_static_assessment. Agents: tests. Batches: 2. Raw finding IDs: 95.

Location: [omniNotes/src/test/java/it/feio/android/omninotes/utils/TagsHelperTest.java:123](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/test/java/it/feio/android/omninotes/utils/TagsHelperTest.java:123).

**Agent-reported impact:** The selection includes index 1 although the list contains only index 0. Also, the returned tag text is never applied to the note before retrieval, so the final absence assertion checks a note that never contained the comma tag. It does not establish comma parsing behavior.

**Recommended fix:** Select only index 0 and apply the returned text to the note before checking retrieval.

**Suggested regression test:** Add "#comma,comma" using selection {0}, append the returned text to the note, and assert the exact intended parsed tag set. Test invalid selection indices separately if supported.

### ON-60. [VERIFY] Note parceling loses the database ID

Severity: HIGH (highest agent rating). Status: requires_dependency_verification. Agents: quality, tests. Batches: 4, 5. Raw finding IDs: 11, 73.

Location: [omniNotes/src/main/java/it/feio/android/omninotes/models/Note.java:169](/Users/krishnakumar/Documents/github/Omni-Notes/omniNotes/src/main/java/it/feio/android/omninotes/models/Note.java:169).

**Assessment / preconditions:** Deferred, not a confirmed defect: Note extends an external BaseNote whose identity semantics were not present in the snapshot. setCreation may restore the identity used by get_id. Confirm the dependency implementation and perform a real Parcel round-trip before accepting the agent’s high-severity claim.

**Agent-reported impact:** Neither writeToParcel nor the parcel constructor preserves the note ID. Existing notes passed through an Intent or restored fragment arguments therefore lose their database identity. SnoozeActivity subsequently saves such notes or forwards note.get_id(), potentially updating the wrong identity or creating a duplicate.

**Recommended fix:** Write the note ID into the parcel and read it back in the matching position.

**Suggested regression test:** Round-trip a persisted note through Parcel and assert that its ID and all other persisted fields remain equal.

## Regression-test and remediation plan

1. **Authorization and secrecy:** cancelled/failed password setting changes must not persist; preferences/log output must omit secret material; locked note read/write must use an appropriately managed key. Fault-inject cryptographic errors and require explicit failures without plaintext persistence. Version encryption formats and test migration/restore compatibility.
2. **Migration integrity:** construct legacy databases with duplicate creation timestamps, mixed trash state, attachment rows, and past/future reminders. Inject an SQL failure and require rollback with original data intact. Assert nonzero row counts and preservation of content, IDs, and attachment bytes, not just allMatch over possibly empty collections.
3. **Backups and attachments:** persist only actually granted read/write URI permissions; verify access after process restart/reboot where appropriate. Inject storage-full, unreadable JSON, missing attachment directories, and mid-copy failures. Verify no success result for partial backups and no replacement of good data by corrupt/empty imports.
4. **Concurrency and identity:** freeze the clock and insert multiple attachments, fault-inject database updates, then verify unique rows/files and transaction release. Determine BaseNote identity semantics before changing parcel serialization.
5. **Android lifecycle:** stop/start activities, recreate settings/category screens, test worker-thread callbacks and absent viewer applications, and exercise malformed external intents. Verify the app handles failures without crashing.
6. **Reminders:** cover denied exact-alarm access, undo after trash, stale queued broadcasts, recurrence snoozing, local midnight, and daylight-saving boundaries.
7. **Test suite reliability:** repair retry deadlines, assert actual Espresso view visibility, wait explicitly for camera events, and verify persisted note state after creation.

## Execution provenance

| Batch | Files | Bytes | Run ID | Status | Keenable | Sources | Actual models |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 53 | 222756 | `33d2d3ce-1dc7-4700-a8a9-7578b833010b` | complete | ok | 6 | gpt-6.1-sol |
| 2 | 56 | 222724 | `391284c4-77b2-47a9-883e-6eb26673019a` | complete | ok | 6 | gpt-6.1-sol |
| 3 | 59 | 222712 | `1b686ab7-1910-43ce-be92-d593db92e733` | complete | ok | 6 | gpt-6.1-sol |
| 4 | 63 | 222733 | `a4b7a533-14ab-41d7-9c9a-807899f2f2a1` | complete | ok | 6 | gpt-6.1-sol |
| 5 | 60 | 222769 | `4d788c4f-69b4-4215-aaa5-8dd84184a656` | complete | ok | 6 | gpt-6.1-sol |

Each batch JSON retains snapshot hashes, durations, requested/actual model provenance, citation corrections, limitations, and retrieved snippets. Keenable queries were generic language/anti-pattern searches, without repository text or filenames. Sources are untrusted guidance; all retained findings still passed repository citation validation.

## Limitations and interpretation

- Exact source citations validate location, not the truth of the model’s reasoning. Detailed findings preserve agent wording while assessment notes qualify important claims.
- Code split across batches reduces integration context. Broad absence-of-tests claims must be checked against the entire test suite before adding tests.
- Legacy migration defects apply only to relevant upgrade paths. Security findings require the documented access or data-exposure preconditions.
- The deferred Parcel-ID finding depends on an external BaseNote implementation; no claim of confirmed note-identity loss is made here.
- No live CVE/dependency audit was performed, and no absence of other vulnerabilities is implied.
- Published here means report artifacts saved in the local coding-agent project; nothing was posted to the upstream Omni-Notes repository.

## Report artifacts

- [All 95 findings: raw Markdown](review-report-omni-notes-raw.md)
- [Combined raw JSON and per-agent provenance](review-report-omni-notes.json)
- [Consolidated prioritized groups: JSON](prioritized-findings.json)
- [Exact scope and batch membership](scope.json)
- Batch 1: [Markdown](batch-1.md) / [JSON](batch-1.json)
- Batch 2: [Markdown](batch-2.md) / [JSON](batch-2.json)
- Batch 3: [Markdown](batch-3.md) / [JSON](batch-3.json)
- Batch 4: [Markdown](batch-4.md) / [JSON](batch-4.json)
- Batch 5: [Markdown](batch-5.md) / [JSON](batch-5.json)
