# Expense Tracker mobile app — prioritized review

## Executive assessment

The three-agent review completed successfully. It retained 24 source-cited findings, consolidated here into **13 distinct issues: two high and eleven medium**. The raw counts are five high and nineteen medium because multiple agents reported the same underlying problems under different titles. No critical findings were returned; this is not proof that none exist.

Address biometric access control and session identity first. Next remove sensitive logging, migrate bearer tokens to Keychain, and fix input-triggered crashes. The app has additional transaction-date defects and unfinished save actions.

## Scope and provenance

- Repository: `/Users/krishnakumar/Documents/github/Expense-Tracker-App` ([upstream](https://github.com/abdorizak/Expense-Tracker-App)).
- Revision: `4dfa91809f9f9680c8d8c813b500ca1f8b996bb0`; checkout was clean at review start.
- Snapshot: 64 Swift files, 234,057 bytes.
- Snapshot SHA-256: `83ab6449ed7aab7c754f304211b83cc5e8bb9d96ec92f5933d5d63953883c24d`.
- Run ID: `f319884c-f806-4efa-8476-8d2d8edcd9f4`; completed `2026-10-25T01:12:53.848129+00:00`.
- Duration: 46.108 seconds; all three agents succeeded.
- Backend: signed-in Codex CLI; provider-reported actual model: **gpt-6.1-sol** for all agents. Fireworks credentials were unavailable in the invoking environment.
- Agent 1 enrichment: **Keenable status ok**, six retained sources, generic Swift anti-pattern search.
- Swift source selection and Swift-specific knowledge queries were added to the review engine; its 133 regression tests pass. The target app was not changed.
- Static review only: no app build, simulator run, XCTest execution, API probing, or coverage measurement.
- Agent snapshot excludes Xcode configuration, assets, nibs, storyboards, dependency resolution, and the server. Separate read-only inspection found one app target and no XCTest target in project.pbxproj.

## Prioritized findings

| Order | Priority | Severity | Issue | Agents |
| --- | --- | --- | --- | --- |
| 1 | P1 | HIGH | Biometric authentication fails open | quality, security, tests |
| 2 | P1 | HIGH | Network manager retains the previous session's user ID | quality, tests |
| 3 | P2 | MEDIUM | Login credentials are written to console output | quality, security, tests |
| 4 | P2 | MEDIUM | Bearer access token is persisted in UserDefaults | security |
| 5 | P2 | MEDIUM | Non-numeric transaction amounts crash during submission | quality, tests |
| 6 | P2 | MEDIUM | Nonnumeric signup PIN crashes instead of showing validation | quality, tests |
| 7 | P2 | MEDIUM | Selected transaction date is never sent to the server | quality, tests |
| 8 | P2 | MEDIUM | Date picker ignores its selected day | quality, tests |
| 9 | P2 | MEDIUM | Change Password Save action performs no operation | quality, tests |
| 10 | P2 | MEDIUM | Edit-profile Save button has no action | quality |
| 11 | P2 | MEDIUM | Profile header rebuilds its nib on every layout | quality, tests |
| 12 | P2 | MEDIUM | Empty transaction refresh leaves previously displayed rows intact | quality |
| 13 | P2 | MEDIUM | Stored settings handlers retain ProfileVC indefinitely | quality |

P1 means address before release; P2 means the next remediation wave. These are remediation priorities, separate from the original severity ratings. Ordering within P2 places credential handling and crashes first.

### 1. [P1 / HIGH] Biometric authentication fails open

Location: [Expense Tracker/Custom Views/TabBar Controller/TabBarVC.swift:39](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Custom%20Views/TabBar%20Controller/TabBarVC.swift:39) · Agents: quality, security, tests · Raw findings: 1, 2, 3.

**Impact and failure scenario:** The tabs are already installed before authentication. Cancelling or failing biometrics only displays a dismissible alert, leaving financial data and transaction actions accessible. When biometrics cannot be evaluated, execution likewise leaves access open.

**Recommended fix:** Gate installation or interaction of protected controllers behind successful authentication, and retain a locked screen on failure or biometric unavailability.

**Regression test:** Enable biometric authentication, launch with a stored session, then cancel authentication or simulate biometric lockout. Assert that dashboard data and transaction actions remain inaccessible.

**Source evidence:**

````swift
                        if !success {
                            // Handle authentication failure
                            let alert = UIAlertController(title: "Authentication Failed", message: "Please try again.", preferredStyle: .alert)
                            alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
                            self?.present(alert, animated: true, completion: nil)
                        }
````

### 2. [P1 / HIGH] Network manager retains the previous session's user ID

Location: [Expense Tracker/Network Manager/NetworkManager.swift:14](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Network%20Manager/NetworkManager.swift:14) · Agents: quality, tests · Raw findings: 4, 5.

**Impact and failure scenario:** The singleton snapshots the user ID once, while login updates UserDefaults. Signing up initializes this singleton before login, potentially retaining nil and later crashing at userID! when saving a transaction. Switching accounts retains the old account's ID in request paths and bodies.

**Recommended fix:** Resolve the current user ID per request, require it with a throwing guard, and clear session identity on logout.

**Regression test:** Initialize NetworkManager before login, then authenticate and save a transaction; assert the authenticated ID is sent without a crash. Log out of account A and into B in the same process; assert every subsequent request uses B's ID.

**Source evidence:**

````swift
    private let userID          = UserDefaults.standard.string(forKey: "user_id")
````

### 3. [P2 / MEDIUM] Login credentials are written to console output

Location: [Expense Tracker/Network Manager/AuthManager.swift:38](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Network%20Manager/AuthManager.swift:38) · Agents: quality, security, tests · Raw findings: 19, 20, 21.

**Impact and failure scenario:** Printing LoginBody exposes its username/email and plaintext password. Anyone with access to captured application console output or diagnostic logs containing this output can recover credentials, including unsuccessful login attempts.

**Recommended fix:** Remove credential-body logging. Log only non-sensitive authentication outcomes.

**Regression test:** Log in using distinctive test credentials while capturing console output; assert that neither the password nor the serialized credential body appears.

**Source evidence:**

````swift
        let body = LoginBody(userCredential: usernameOrEmail, password: password)
        print("DEBUG:\(body)")
````

### 4. [P2 / MEDIUM] Bearer access token is persisted in UserDefaults

Location: [Expense Tracker/Network Manager/AuthManager.swift:84](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Network%20Manager/AuthManager.swift:84) · Agents: security · Raw findings: 22.

**Impact and failure scenario:** The access token is stored in ordinary application preferences and later used as a bearer credential. An attacker who obtains readable app-container preferences or a backup containing them can extract and replay the token while it remains valid.

**Recommended fix:** Store the token in Keychain with an appropriate device-only accessibility policy, migrate existing preference values, and delete the Keychain entry on logout.

**Regression test:** After login, assert that access_token is absent from UserDefaults and available only through Keychain; after logout, assert that the Keychain entry is removed.

**Source evidence:**

````swift
    private func catchToken(result: LoginResponse) {
        UserDefaults.standard.setValue(result.accessToken, forKey: "access_token")
        UserDefaults.standard.setValue(result.userInfo, forKey: "user_id")
    }
````

### 5. [P2 / MEDIUM] Non-numeric transaction amounts crash during submission

Location: [Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237) · Agents: quality, tests · Raw findings: 8, 11.

**Impact and failure scenario:** Validation checks only whether the amount is empty. The initial "$0" value and pasted non-numeric text pass that check but fail Double conversion, causing a force-unwrap trap outside recoverable error handling.

**Recommended fix:** Parse and validate a finite amount before starting the task, and present a validation error when parsing fails.

**Regression test:** Fill all other transaction fields and submit with the untouched "$0" amount, then with pasted "abc". Assert a validation alert appears, no network request occurs, and the app remains responsive.

**Source evidence:**

````swift
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

### 6. [P2 / MEDIUM] Nonnumeric signup PIN crashes instead of showing validation

Location: [Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Controllers/Login%20SingUp/SingUpVC.swift:165) · Agents: quality, tests · Raw findings: 6, 7.

**Impact and failure scenario:** Signup validation only checks that the PIN is nonempty. Its text field accepts ordinary text, and the length delegate is never assigned. Entering abc or an integer outside Int's range passes validation and traps at the forced conversion; do/catch cannot recover from this trap.

**Recommended fix:** Validate a four-digit PIN and safely unwrap its conversion before starting the request. Assign a PIN-specific input delegate rather than applying a four-character limit to all signup fields.

**Regression test:** Submit otherwise valid signup details with PIN abc, an oversized integer, and five digits. Assert that each produces a validation error without issuing a request or crashing.

**Source evidence:**

````swift
                    let signUpResult = try await NetworkManager.shared.Signup(fullname: fullnameTextFeild.text!, email: emailTextFeild.text!, mobile: phoneTextFeild.text!, username: usernameTextFeild.text!, pin: Int(pinTextFeild.text!)!, passowrd: passwordTextFeild.text!)
````

### 7. [P2 / MEDIUM] Selected transaction date is never sent to the server

Location: [Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237) · Agents: quality, tests · Raw findings: 9, 10.

**Impact and failure scenario:** The form requires a date, but this call passes only type, title, description, and amount. The supplied makeTransaction implementation and TransactionBody also omit a date, so changing the date cannot affect the saved transaction.

**Recommended fix:** Retain the selected Date and pass it through the network API into the encoded transaction body.

**Regression test:** Create otherwise identical transactions with two different selected dates and capture their request bodies. Assert each contains its selected date and that fetching the saved transactions preserves those dates.

**Source evidence:**

````swift
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

### 8. [P2 / MEDIUM] Date picker ignores its selected day

Location: [Expense Tracker/Utilits/DatePicker.swift:91](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Utilits/DatePicker.swift:91) · Agents: quality, tests · Raw findings: 23, 24.

**Impact and failure scenario:** The selected day is checked but never used. chooseTime is generated from today's date, so selecting tomorrow still sends a Date for today to the callback and displays the wrong day.

**Recommended fix:** Combine calendar date components from days[dayIndex] with time components from the selected time before invoking didSelectDates.

**Regression test:** Select tomorrow and 10 AM. Assert that the callback date represents tomorrow at 10 AM in the current calendar and time zone.

**Source evidence:**

````swift
        guard days.indices.contains(dayIndex),
              chooseTime.indices.contains(chooseTimeTimeIndex) else { return }
        
        let timeChoosed = chooseTime[chooseTimeTimeIndex]
        
        didSelectDates?(timeChoosed)
````

### 9. [P2 / MEDIUM] Change Password Save action performs no operation

Location: [Expense Tracker/Controllers/ProfileViews/ChangePasswordVC.swift:115](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Controllers/ProfileViews/ChangePasswordVC.swift:115) · Agents: quality, tests · Raw findings: 14, 15.

**Impact and failure scenario:** The visible Save button invokes this empty handler. Entering current and new passwords cannot change the account password or produce any feedback.

**Recommended fix:** Implement password validation and the password-change request with success and failure feedback, or disable the unfinished action.

**Regression test:** Enter the correct current password and matching valid new passwords, then tap Save. Assert the change request is sent and success is reported. For mismatched confirmation or an incorrect current password, assert an error is shown and the password remains unchanged.

**Source evidence:**

````swift
    @objc func didTapSave() {
        // this will check first current password the will change password by checking password
        
    }
````

### 10. [P2 / MEDIUM] Edit-profile Save button has no action

Location: [Expense Tracker/Controllers/ProfileViews/EditProfileVC.swift:302](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Controllers/ProfileViews/EditProfileVC.swift:302) · Agents: quality · Raw findings: 16.

**Impact and failure scenario:** The complete controller never attaches an action to saveBtn or submits profile changes. Edited fields and the selected avatar remain local UI state and are lost when the controller is dismissed.

**Recommended fix:** Attach a save handler that validates and persists the profile and avatar, then updates the displayed profile after success.

**Regression test:** Change the name and avatar and tap Save. Assert that persistence is invoked and reopening the profile shows the saved values.

**Source evidence:**

````swift
    func configSavebtn() {
        saveBtn.setTitle("Save", for: .normal)
        contentView.addSubview(saveBtn)
        NSLayoutConstraint.activate([
````

### 11. [P2 / MEDIUM] Profile header rebuilds its nib on every layout

Location: [Expense Tracker/Custom Views/UIView/ProfileHeaderView.swift:25](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Custom%20Views/UIView/ProfileHeaderView.swift:25) · Agents: quality, tests · Raw findings: 17, 18.

**Impact and failure scenario:** This repeated-initialization anti-pattern calls commonInit on every layout, loading and adding another nib-backed content view and activating new constraints. It also overwrites the supplied user's name with the hardcoded name at line 60. Layout therefore changes displayed identity and accumulates views.

**Recommended fix:** Load the nib and install constraints once during initialization. Limit layoutSubviews to geometry-dependent updates, and remove the hardcoded name assignment.

**Regression test:** Construct a header with a distinct name and perform several layout passes. Assert that the name remains unchanged and the subview and constraint counts remain stable.

**Source evidence:**

````swift
    override func layoutSubviews() {
        super.layoutSubviews()
        commonInit()
    }
````

### 12. [P2 / MEDIUM] Empty transaction refresh leaves previously displayed rows intact

Location: [Expense Tracker/Controllers/Main/HomeVC.swift:144](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Controllers/Main/HomeVC.swift:144) · Agents: quality · Raw findings: 12.

**Impact and failure scenario:** When a refresh changes a previously nonempty result to an empty array, the table is not reloaded or hidden. Its existing rows remain displayed despite the backing array being empty, and the empty-state label is behind the table in the configured view hierarchy.

**Recommended fix:** Reload the table for every successful response and explicitly toggle visibility between the table and empty-state label.

**Regression test:** Load several transactions, then refresh with an empty response. Assert zero displayed rows and a visible empty-state message; refresh with data again and assert the message is hidden.

**Source evidence:**

````swift
            self.transaction = transactions.transaction
            if !transaction.isEmpty {
                configTableView()
                self.tableView.reloadDataOnMainThread()
            } else {
                layoutLable("This user doesn't have any Transactions. Go and make Expenses or Income 😀.")
            }
````

### 13. [P2 / MEDIUM] Stored settings handlers retain ProfileVC indefinitely

Location: [Expense Tracker/Controllers/Main/ProfileVC.swift:88](/Users/krishnakumar/Documents/github/Expense-Tracker-App/Expense%20Tracker/Controllers/Main/ProfileVC.swift:88) · Agents: quality · Raw findings: 13.

**Impact and failure scenario:** This strong-reference-cycle anti-pattern forms ProfileVC → models → handler → ProfileVC. Multiple stored handlers capture self this way, so dismissing the profile does not release it or its transaction data. Repeated profile presentations accumulate retained controllers.

**Recommended fix:** Use weak self captures in every handler stored in models, or store action identifiers and dispatch them from didSelectRowAt.

**Regression test:** Present and dismiss ProfileVC while retaining only a weak reference. Assert that the weak reference becomes nil after dismissal.

**Source evidence:**

````swift
        models.append(Sections(options: [
            SettingOpetions(icon: Images.edityourProfile, title: "Edit Profile", handler: {
                let editProfileVC = EditProfileVC()
                editProfileVC.title = "Edit Profile"
                return self.navigationController?.pushViewController(editProfileVC, animated: true)
            }),
````

## Missing-test implementation plan

No Swift tests were present in the selected source. Separate project inspection also found no XCTest target. Create unit and UI-test targets, then introduce injectable session storage, authentication, networking, and biometric boundaries so tests can be deterministic and avoid production services.

| Area | Required scenarios | Expected result |
| --- | --- | --- |
| Biometric gate | Success, cancel, failure, unavailable, lockout | Protected screens unlock only on authorized success |
| Session lifecycle | Manager initialized before login; A logs out and B logs in; missing ID | Current identity in every request, no nil trap, old identity cleared |
| Credential handling | Sentinel password logging; token write/read/delete | No secrets in output or preferences; Keychain cleared on logout |
| Amount validation | Untouched $0, pasted text, invalid/nonfinite values, valid amount | Invalid values rejected before request, no crash |
| Signup PIN | Letters, overflow, wrong length, valid four digits | Validation error or valid submission as appropriate |
| Transaction date | Different day, time zone, encoded request, readback | Selected date survives UI, serialization and persistence |
| Save actions | Password/profile success, validation and network failure | Request and feedback occur; changes persist only on success |
| View lifecycle | Repeat layout, repeated presentation/dismissal | Stable view/constraint counts, correct name, controller deallocation |
| Transaction refresh | Nonempty to empty and back | Correct rows and empty-state visibility |

The raw tests agent supplied nine findings. Additional credential-storage and lifecycle tests above come from quality/security recommendations. Runtime coverage remains unmeasured.

## Remediation sequence

1. Gate financial screens behind authentication and resolve user identity dynamically through a session provider.
2. Remove credential logging, migrate tokens to Keychain, and add logout/migration regressions.
3. Guard input parsing; reject invalid values before starting asynchronous work.
4. Carry transaction dates end to end and implement or disable unfinished save actions.
5. Repair lifecycle, layout, and refresh defects; establish XCTest and UI tests in CI.

## Interpretation and limitations

- Findings were citation-validated and key locations were manually inspected. Runtime consequences remain static assessments pending reproduction.
- The stale identity problem can produce incorrect IDs and a nil crash. Unauthorized cross-account access additionally depends on server-side authorization, which was not reviewed.
- Token extraction requires access to readable preferences or relevant backups; the review did not demonstrate extraction or token replay.
- Credential exposure is to console/diagnostic consumers; no remote log exfiltration was demonstrated.
- The biometric gate assumes an existing signed-in session with biometric protection enabled.
- API date-field names and accepted date formats must be verified against the backend contract.
- Reports do not establish absence of vulnerabilities, nor quantify test coverage. Keenable context is guidance, not repository evidence.

## Keenable sources

- skills/skills/write-swift/SKILL.md at main · emilkowalski/skills — https://github.com/emilkowalski/skills/blob/main/skills/write-swift/SKILL.md
- code-review-skill/reference/swift.md at 4850184dfd7765ea7b3c5c4e9b6cf8e0815ee7cb · awesome-skills/code-review-skill — https://github.com/awesome-skills/code-review-skill/blob/HEAD/reference/swift.md
- claude-code-ios-plugin/skills/code-review-checklist/SKILL.md at main · arimunandar/claude-code-ios-plugin — https://github.com/arimunandar/claude-code-ios-plugin/blob/main/skills/code-review-checklist/SKILL.md
- Swift-6-Agent-Skill/swift-6-agent-skill/SKILL.md at 307e013374525ec75debb55d8936e7d40ef7709f · pchelnikov/Swift-6-Agent-Skill — https://github.com/pchelnikov/Swift-6-Agent-Skill/blob/307e013374525ec75debb55d8936e7d40ef7709f/swift-6-agent-skill/SKILL.md
- ECC/agents/swift-reviewer.md at 1a2cd81ed34cbb6fc826eafeb23eea27234c664e · affaan-m/ECC — https://github.com/affaan-m/ECC/blob/1a2cd81ed34cbb6fc826eafeb23eea27234c664e/agents/swift-reviewer.md
- GitHub - Fueled/swift-style-guide: Official Swift language style guide used at Fueled (Swift 6, language rules only). — https://github.com/fueled/swift-style-guide

## Full agent reports

- [Raw Markdown: all 24 retained findings](review-report-expense-tracker-raw.md)
- [JSON: per-agent findings, evidence, provenance, limitations, and retrieved snippets](review-report-expense-tracker.json)
