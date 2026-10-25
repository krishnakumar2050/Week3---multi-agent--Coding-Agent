# Code review report

Status: **complete**

Static test-gap analysis only; tests were not executed and coverage was not measured.

critical: 0 | high: 5 | medium: 19 | low: 0 | info: 0

Run: `f319884c-f806-4efa-8476-8d2d8edcd9f4` · Schema: 1.0

Repository: `/Users/krishnakumar/Documents/github/Expense-Tracker-App`

Snapshot SHA-256: `83ab6449ed7aab7c754f304211b83cc5e8bb9d96ec92f5933d5d63953883c24d`

Completed: 2026-10-25T01:12:53.848129+00:00 · Duration: 46.108 seconds

## Model provenance

| Agent | Requested model | Actual model | Evidence |
| --- | --- | --- | --- |
| quality | CLI default | gpt-6.1-sol | codex_cli_startup |
| security | CLI default | gpt-6.1-sol | codex_cli_startup |
| tests | CLI default | gpt-6.1-sol | codex_cli_startup |

## Agent 1 anti-pattern knowledge

Keenable status: ok

- skills/skills/write-swift/SKILL.md at main · emilkowalski/skills — https://github.com/emilkowalski/skills/blob/main/skills/write-swift/SKILL.md
- code-review-skill/reference/swift.md at 4850184dfd7765ea7b3c5c4e9b6cf8e0815ee7cb · awesome-skills/code-review-skill — https://github.com/awesome-skills/code-review-skill/blob/HEAD/reference/swift.md
- claude-code-ios-plugin/skills/code-review-checklist/SKILL.md at main · arimunandar/claude-code-ios-plugin — https://github.com/arimunandar/claude-code-ios-plugin/blob/main/skills/code-review-checklist/SKILL.md
- Swift-6-Agent-Skill/swift-6-agent-skill/SKILL.md at 307e013374525ec75debb55d8936e7d40ef7709f · pchelnikov/Swift-6-Agent-Skill — https://github.com/pchelnikov/Swift-6-Agent-Skill/blob/307e013374525ec75debb55d8936e7d40ef7709f/swift-6-agent-skill/SKILL.md
- ECC/agents/swift-reviewer.md at 1a2cd81ed34cbb6fc826eafeb23eea27234c664e · affaan-m/ECC — https://github.com/affaan-m/ECC/blob/1a2cd81ed34cbb6fc826eafeb23eea27234c664e/agents/swift-reviewer.md
- GitHub - Fueled/swift-style-guide: Official Swift language style guide used at Fueled (Swift 6, language rules only). — https://github.com/fueled/swift-style-guide

External guidance supplements source analysis; it is not repository evidence.

## 1. [HIGH] Biometric authentication fails open

Location: `Expense Tracker/Custom Views/TabBar Controller/TabBarVC.swift:39` · Agents: quality

The tabs are already installed before authentication. Cancelling or failing biometrics only displays a dismissible alert, leaving financial data and transaction actions accessible. When biometrics cannot be evaluated, execution likewise leaves access open.

Fix: Gate installation or interaction of protected controllers behind successful authentication, and retain a locked screen on failure or biometric unavailability.

Suggested test: Enable biometric authentication, launch with a stored session, then cancel authentication or simulate biometric lockout. Assert that dashboard data and transaction actions remain inaccessible.

Evidence:

````
                        if !success {
                            // Handle authentication failure
                            let alert = UIAlertController(title: "Authentication Failed", message: "Please try again.", preferredStyle: .alert)
                            alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
                            self?.present(alert, animated: true, completion: nil)
                        }
````

## 2. [HIGH] Biometric authentication failure leaves protected screens accessible

Location: `Expense Tracker/Custom Views/TabBar Controller/TabBarVC.swift:39` · Agents: tests

The tabs are installed before authentication. Failure only displays a dismissible alert, and unavailable biometrics only logs a message. Users can therefore access financial data despite enabling biometric protection.

Fix: Gate protected content behind successful authentication and retain a locked screen on cancellation, failure, or unavailable biometrics.

Suggested test: Enable biometric protection and simulate cancellation, authentication failure, and unavailable biometrics. Assert that dismissing any alert never exposes dashboard data or transaction controls; assert successful authentication unlocks them.

Evidence:

````
                        if !success {
                            // Handle authentication failure
                            let alert = UIAlertController(title: "Authentication Failed", message: "Please try again.", preferredStyle: .alert)
                            alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
                            self?.present(alert, animated: true, completion: nil)
                        }
````

## 3. [HIGH] Biometric authentication failure leaves the app accessible

Location: `Expense Tracker/Custom Views/TabBar Controller/TabBarVC.swift:39` · Agents: security

The protected tabs are installed before authentication. With an existing signed-in session and Face ID enabled, someone holding the unlocked device can cancel or fail authentication, dismiss this alert, and access financial data and transaction controls. Biometric unavailability also only prints a message and permits access.

Fix: Keep protected content inaccessible until authentication succeeds. On cancellation, failure, or biometric unavailability, retain a blocking authentication screen or require account authentication.

Suggested test: With a saved session and Face ID enabled, cancel biometric authentication and dismiss the alert; assert that financial data and transaction controls remain inaccessible. Repeat with biometrics unavailable.

Evidence:

````
                        if !success {
                            // Handle authentication failure
                            let alert = UIAlertController(title: "Authentication Failed", message: "Please try again.", preferredStyle: .alert)
                            alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
                            self?.present(alert, animated: true, completion: nil)
                        }
````

## 4. [HIGH] Network manager retains the previous session's user ID

Location: `Expense Tracker/Network Manager/NetworkManager.swift:14` · Agents: tests

The singleton snapshots the user ID once, while login updates UserDefaults. Signing up initializes this singleton before login, potentially retaining nil and later crashing at userID! when saving a transaction. Switching accounts retains the old account's ID in request paths and bodies.

Fix: Resolve the current user ID per request, require it with a throwing guard, and clear session identity on logout.

Suggested test: Initialize NetworkManager before login, then authenticate and save a transaction; assert the authenticated ID is sent without a crash. Log out of account A and into B in the same process; assert every subsequent request uses B's ID.

Evidence:

````
    private let userID          = UserDefaults.standard.string(forKey: "user_id")
````

## 5. [HIGH] Network singleton permanently caches the first user ID

Location: `Expense Tracker/Network Manager/NetworkManager.swift:14` · Agents: quality

This hidden session-state snapshot never changes after singleton initialization. Signing up initializes NetworkManager before login stores a user ID, so later dashboard requests use N/A and makeTransaction force-unwraps nil. Logging out and signing into another account in the same process instead keeps the previous account's ID.

Fix: Resolve the current user ID for each request through a session provider, reject missing IDs with a thrown error, and clear session identity on logout.

Suggested test: Initialize NetworkManager before login, then log in and create a transaction; assert that the new ID is used without a crash. Repeat after switching between two accounts.

Evidence:

````
    private let userID          = UserDefaults.standard.string(forKey: "user_id")
````

## 6. [MEDIUM] Nonnumeric signup PIN crashes instead of showing validation

Location: `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` · Agents: quality

Signup validation only checks that the PIN is nonempty. Its text field accepts ordinary text, and the length delegate is never assigned. Entering abc or an integer outside Int's range passes validation and traps at the forced conversion; do/catch cannot recover from this trap.

Fix: Validate a four-digit PIN and safely unwrap its conversion before starting the request. Assign a PIN-specific input delegate rather than applying a four-character limit to all signup fields.

Suggested test: Submit otherwise valid signup details with PIN abc, an oversized integer, and five digits. Assert that each produces a validation error without issuing a request or crashing.

Evidence:

````
                    let signUpResult = try await NetworkManager.shared.Signup(fullname: fullnameTextFeild.text!, email: emailTextFeild.text!, mobile: phoneTextFeild.text!, username: usernameTextFeild.text!, pin: Int(pinTextFeild.text!)!, passowrd: passwordTextFeild.text!)
````

## 7. [MEDIUM] Signup accepts PIN text that crashes integer conversion

Location: `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` · Agents: tests

Signup validation only requires a nonempty PIN. The field has no assigned delegate enforcing its declared length restriction, and its initializer does not select a numeric keyboard. Non-numeric or overflowing input therefore reaches a forced Int conversion and crashes.

Fix: Validate the PIN's digit count and numeric conversion explicitly before submission, using a guarded conversion.

Suggested test: Populate otherwise valid signup fields with matching passwords. Try PINs "abcd", "12345", and an integer-overflowing digit string. Assert validation rejects each without sending a request or crashing; assert a four-digit PIN is accepted.

Evidence:

````
                    let signUpResult = try await NetworkManager.shared.Signup(fullname: fullnameTextFeild.text!, email: emailTextFeild.text!, mobile: phoneTextFeild.text!, username: usernameTextFeild.text!, pin: Int(pinTextFeild.text!)!, passowrd: passwordTextFeild.text!)
````

## 8. [MEDIUM] Non-numeric transaction amounts crash during submission

Location: `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` · Agents: tests

Validation checks only whether the amount is empty. The initial "$0" value and pasted non-numeric text pass that check but fail Double conversion, causing a force-unwrap trap outside recoverable error handling.

Fix: Parse and validate a finite amount before starting the task, and present a validation error when parsing fails.

Suggested test: Fill all other transaction fields and submit with the untouched "$0" amount, then with pasted "abc". Assert a validation alert appears, no network request occurs, and the app remains responsive.

Evidence:

````
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

## 9. [MEDIUM] Selected transaction date is never sent to the server

Location: `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` · Agents: tests

The form requires a date, but this call passes only type, title, description, and amount. The supplied makeTransaction implementation and TransactionBody also omit a date, so changing the date cannot affect the saved transaction.

Fix: Retain the selected Date and pass it through the network API into the encoded transaction body.

Suggested test: Create otherwise identical transactions with two different selected dates and capture their request bodies. Assert each contains its selected date and that fetching the saved transactions preserves those dates.

Evidence:

````
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

## 10. [MEDIUM] Selected transaction date is omitted from the request

Location: `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` · Agents: quality

The form requires a selected date, but the request passes only type, title, description, and amount. TransactionBody also has no date property, so the selected date cannot affect the saved transaction.

Fix: Keep the selected Date as model state and pass it through makeTransaction and TransactionBody using the API's date representation.

Suggested test: Select a date different from today and save. Assert that the outgoing request and subsequently retrieved transaction contain that selected date.

Evidence:

````
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

## 11. [MEDIUM] Transaction amount conversion can crash on accepted input

Location: `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` · Agents: quality

Validation checks only emptiness, while the initial amount is the nonempty string $0. Completing the other fields without editing that amount, or pasting nonnumeric text, reaches Double(...)! and crashes.

Fix: Parse and validate a finite monetary amount before starting the task, and display $0 as a placeholder or format it separately from the numeric input.

Suggested test: Complete the form while leaving the initial $0 untouched, then repeat with pasted abc. Assert a validation message and no crash or network request.

Evidence:

````
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

## 12. [MEDIUM] Empty transaction refresh leaves previously displayed rows intact

Location: `Expense Tracker/Controllers/Main/HomeVC.swift:144` · Agents: quality

When a refresh changes a previously nonempty result to an empty array, the table is not reloaded or hidden. Its existing rows remain displayed despite the backing array being empty, and the empty-state label is behind the table in the configured view hierarchy.

Fix: Reload the table for every successful response and explicitly toggle visibility between the table and empty-state label.

Suggested test: Load several transactions, then refresh with an empty response. Assert zero displayed rows and a visible empty-state message; refresh with data again and assert the message is hidden.

Evidence:

````
            self.transaction = transactions.transaction
            if !transaction.isEmpty {
                configTableView()
                self.tableView.reloadDataOnMainThread()
            } else {
                layoutLable("This user doesn't have any Transactions. Go and make Expenses or Income 😀.")
            }
````

## 13. [MEDIUM] Stored settings handlers retain ProfileVC indefinitely

Location: `Expense Tracker/Controllers/Main/ProfileVC.swift:88` · Agents: quality

This strong-reference-cycle anti-pattern forms ProfileVC → models → handler → ProfileVC. Multiple stored handlers capture self this way, so dismissing the profile does not release it or its transaction data. Repeated profile presentations accumulate retained controllers.

Fix: Use weak self captures in every handler stored in models, or store action identifiers and dispatch them from didSelectRowAt.

Suggested test: Present and dismiss ProfileVC while retaining only a weak reference. Assert that the weak reference becomes nil after dismissal.

Evidence:

````
        models.append(Sections(options: [
            SettingOpetions(icon: Images.edityourProfile, title: "Edit Profile", handler: {
                let editProfileVC = EditProfileVC()
                editProfileVC.title = "Edit Profile"
                return self.navigationController?.pushViewController(editProfileVC, animated: true)
            }),
````

## 14. [MEDIUM] Change Password Save action performs no operation

Location: `Expense Tracker/Controllers/ProfileViews/ChangePasswordVC.swift:115` · Agents: tests

The visible Save button invokes this empty handler. Entering current and new passwords cannot change the account password or produce any feedback.

Fix: Implement password validation and the password-change request with success and failure feedback, or disable the unfinished action.

Suggested test: Enter the correct current password and matching valid new passwords, then tap Save. Assert the change request is sent and success is reported. For mismatched confirmation or an incorrect current password, assert an error is shown and the password remains unchanged.

Evidence:

````
    @objc func didTapSave() {
        // this will check first current password the will change password by checking password
        
    }
````

## 15. [MEDIUM] Change-password Save action performs no operation

Location: `Expense Tracker/Controllers/ProfileViews/ChangePasswordVC.swift:115` · Agents: quality

The visible Save button invokes this empty method. Users can enter current and replacement passwords and tap Save, but no validation, password update, or feedback occurs.

Fix: Implement validation and the password-change request with success and failure feedback, or disable access to the unfinished action.

Suggested test: Enter valid matching replacement passwords and tap Save. Assert that a password-change request occurs and the result is presented.

Evidence:

````
    @objc func didTapSave() {
        // this will check first current password the will change password by checking password
        
    }
````

## 16. [MEDIUM] Edit-profile Save button has no action

Location: `Expense Tracker/Controllers/ProfileViews/EditProfileVC.swift:302` · Agents: quality

The complete controller never attaches an action to saveBtn or submits profile changes. Edited fields and the selected avatar remain local UI state and are lost when the controller is dismissed.

Fix: Attach a save handler that validates and persists the profile and avatar, then updates the displayed profile after success.

Suggested test: Change the name and avatar and tap Save. Assert that persistence is invoked and reopening the profile shows the saved values.

Evidence:

````
    func configSavebtn() {
        saveBtn.setTitle("Save", for: .normal)
        contentView.addSubview(saveBtn)
        NSLayoutConstraint.activate([
````

## 17. [MEDIUM] Profile header rebuilds its nib on every layout

Location: `Expense Tracker/Custom Views/UIView/ProfileHeaderView.swift:25` · Agents: quality

This repeated-initialization anti-pattern calls commonInit on every layout, loading and adding another nib-backed content view and activating new constraints. It also overwrites the supplied user's name with the hardcoded name at line 60. Layout therefore changes displayed identity and accumulates views.

Fix: Load the nib and install constraints once during initialization. Limit layoutSubviews to geometry-dependent updates, and remove the hardcoded name assignment.

Suggested test: Construct a header with a distinct name and perform several layout passes. Assert that the name remains unchanged and the subview and constraint counts remain stable.

Evidence:

````
    override func layoutSubviews() {
        super.layoutSubviews()
        commonInit()
    }
````

## 18. [MEDIUM] Profile header reloads its nib and overwrites the user's name on layout

Location: `Expense Tracker/Custom Views/UIView/ProfileHeaderView.swift:25` · Agents: tests

commonInit loads and adds another content view, activates constraints, and assigns the hardcoded name "Abdorizak Abdalla Hassan". Each layout therefore accumulates content views and replaces the name supplied by the initializer.

Fix: Load the nib and install constraints once during initialization. Restrict layoutSubviews to geometry updates and remove the hardcoded name assignment.

Suggested test: Initialize the header with "Alice Example" and perform several layout passes. Assert the displayed name remains "Alice Example" and the number of content subviews and installed constraints stays constant.

Evidence:

````
    override func layoutSubviews() {
        super.layoutSubviews()
        commonInit()
    }
````

## 19. [MEDIUM] Login credentials are written to console output

Location: `Expense Tracker/Network Manager/AuthManager.swift:38` · Agents: security

Printing LoginBody exposes its username/email and plaintext password. Anyone with access to captured application console output or diagnostic logs containing this output can recover credentials, including unsuccessful login attempts.

Fix: Remove credential-body logging. Log only non-sensitive authentication outcomes.

Suggested test: Log in using distinctive test credentials while capturing console output; assert that neither the password nor the serialized credential body appears.

Evidence:

````
        let body = LoginBody(userCredential: usernameOrEmail, password: password)
        print("DEBUG:\(body)")
````

## 20. [MEDIUM] Login credentials are written to logs

Location: `Expense Tracker/Network Manager/AuthManager.swift:38` · Agents: quality

Printing LoginBody includes its stored password and user credential. Every password login therefore exposes plaintext credentials to application logs, including builds where this unconditional print remains enabled.

Fix: Remove the body logging and log only nonsensitive request metadata.

Suggested test: Log in with a distinctive test password while capturing application output. Assert that neither the password nor the serialized credential body appears.

Evidence:

````
        let body = LoginBody(userCredential: usernameOrEmail, password: password)
        print("DEBUG:\(body)")
````

## 21. [MEDIUM] Login writes plaintext credentials to logs

Location: `Expense Tracker/Network Manager/AuthManager.swift:38` · Agents: tests

Printing LoginBody includes its stored password and user credential. Every password login therefore exposes credentials to console logs.

Fix: Remove the credential-body log and log only non-sensitive request metadata.

Suggested test: Log in with distinctive username and password sentinel values while capturing application logs. Assert neither value appears in the logs.

Evidence:

````
        let body = LoginBody(userCredential: usernameOrEmail, password: password)
        print("DEBUG:\(body)")
````

## 22. [MEDIUM] Bearer access token is persisted in UserDefaults

Location: `Expense Tracker/Network Manager/AuthManager.swift:84` · Agents: security

The access token is stored in ordinary application preferences and later used as a bearer credential. An attacker who obtains readable app-container preferences or a backup containing them can extract and replay the token while it remains valid.

Fix: Store the token in Keychain with an appropriate device-only accessibility policy, migrate existing preference values, and delete the Keychain entry on logout.

Suggested test: After login, assert that access_token is absent from UserDefaults and available only through Keychain; after logout, assert that the Keychain entry is removed.

Evidence:

````
    private func catchToken(result: LoginResponse) {
        UserDefaults.standard.setValue(result.accessToken, forKey: "access_token")
        UserDefaults.standard.setValue(result.userInfo, forKey: "user_id")
    }
````

## 23. [MEDIUM] Date picker ignores its selected day

Location: `Expense Tracker/Utilits/DatePicker.swift:91` · Agents: quality

The selected day is checked but never used. chooseTime is generated from today's date, so selecting tomorrow still sends a Date for today to the callback and displays the wrong day.

Fix: Combine calendar date components from days[dayIndex] with time components from the selected time before invoking didSelectDates.

Suggested test: Select tomorrow and 10 AM. Assert that the callback date represents tomorrow at 10 AM in the current calendar and time zone.

Evidence:

````
        guard days.indices.contains(dayIndex),
              chooseTime.indices.contains(chooseTimeTimeIndex) else { return }
        
        let timeChoosed = chooseTime[chooseTimeTimeIndex]
        
        didSelectDates?(timeChoosed)
````

## 24. [MEDIUM] Date picker ignores the selected day

Location: `Expense Tracker/Utilits/DatePicker.swift:94` · Agents: tests

The callback returns a time constructed using today's date. Although dayIndex is checked, days[dayIndex] is never used, so selecting another day still reports today.

Fix: Combine the selected day's calendar components with the selected time before invoking the callback.

Suggested test: Select tomorrow in component 0 and 10:00 in component 1. Assert the callback's calendar day is tomorrow and its hour and minute are 10:00. Change only the day and assert the callback date changes.

Evidence:

````
        let timeChoosed = chooseTime[chooseTimeTimeIndex]
        
        didSelectDates?(timeChoosed)
````

## Review limitations

- quality: ok
  - Review was limited to the supplied snapshot; no tools, execution, or delegation were used.
  - Server behavior, API contracts, nib contents, deployment targets, and build settings were not supplied, so runtime integration and platform coverage could not be verified.
- security: ok
  - Review was limited to the supplied snapshot; no tools or execution were used.
  - Server-side authorization, PIN rate limits, token expiration and revocation, dependency versions, and backup configuration are not supplied and could not be assessed.
- tests: ok
  - No tests were supplied, so existing test coverage and assertions could not be evaluated.
  - Static review only; no tools were called and no code or tests were executed.
  - Server behavior, project configuration, assets, and nib contents were not supplied; related behavior could not be verified.
