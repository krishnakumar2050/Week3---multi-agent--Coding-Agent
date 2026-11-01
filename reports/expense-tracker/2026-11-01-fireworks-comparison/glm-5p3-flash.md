# Code review report

Status: **complete**

Static test-gap analysis only; tests were not executed and coverage was not measured.

critical: 0 | high: 6 | medium: 4 | low: 1 | info: 0

## Aggregator synthesis

3/3 specialists succeeded; 11 verified finding(s). Highest reported severity: high.

- [HIGH] `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` PIN signup force-unwrap crashes; delegate limiting input is never attached: Set `delegate = self` on each field (or restrict per-field via shouldChangeCharactersIn), validate the PIN is 4 digits with digit-only characterSet before conversion, and transmit the PIN as a String to preserve leading zeros.
- [HIGH] `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` Sign-up force-unwraps PIN conversion; delegate that limits input is never assigned: Set the text field delegates in configVC, and replace the force-unwrap with `guard let pin = Int(pinTextFeild.text ?? "")` plus a validation alert.
- [HIGH] `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` Force-unwrap of amount text crashes on save (default value is "$0"): Parse defensively: strip non-numeric characters, use Double(text.replacingOccurrences(of: "$", with: "")) with guard/optional binding, and show a validation alert on failure instead of crashing.
- [HIGH] `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` Force-unwrap of amount text crashes on the pre-filled value "$0": Use `guard let amountText = expensesAndIncomeTextField.text, let amount = Double(amountText.replacingOccurrences(of: "$", with: ""))` and show a validation alert on failure instead of force-unwrapping.
- [HIGH] `Expense Tracker/Network Manager/AuthManager.swift:39` Login request body including password logged to console: Remove the print or log only non-sensitive fields (e.g., that a login attempt was made).

Run: `8044b2df-5002-4109-ba3d-8be65316a80b` · Schema: 1.0

Repository: `/Users/krishnakumar/Documents/GitHub/Expense-Tracker-App`

Snapshot SHA-256: `83ab6449ed7aab7c754f304211b83cc5e8bb9d96ec92f5933d5d63953883c24d`

Completed: 2026-11-01T10:19:24.715209+00:00 · Duration: 24.958 seconds

## Model provenance

| Agent | Requested model | Actual model | Evidence |
| --- | --- | --- | --- |
| quality | accounts/fireworks/models/glm-5p3-flash | accounts/fireworks/models/glm-5p3-flash | provider_response |
| security | accounts/fireworks/models/glm-5p3-flash | accounts/fireworks/models/glm-5p3-flash | provider_response |
| tests | accounts/fireworks/models/glm-5p3-flash | accounts/fireworks/models/glm-5p3-flash | provider_response |

## 1. [HIGH] PIN signup force-unwrap crashes; delegate limiting input is never attached

Location: `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` · Agents: tests

`Int(pinTextFeild.text!)!` crashes if the PIN contains any non-digit. The UITextFieldDelegate extension (lines 185-192) that limits input to 4 characters is dead code because none of the form fields ever set `delegate = self`. Additionally, an Int-encoded PIN silently drops leading zeros ("0123" is sent as 123), corrupting the credential.

Fix: Set `delegate = self` on each field (or restrict per-field via shouldChangeCharactersIn), validate the PIN is 4 digits with digit-only characterSet before conversion, and transmit the PIN as a String to preserve leading zeros.

Suggested test: Enter PIN "0123" and password "abcdefgh1"; assert signup sends pin "0123" unchanged and does not crash. Enter PIN "12a4"; assert a validation error is shown instead of a crash.

Evidence:

````
                    let signUpResult = try await NetworkManager.shared.Signup(fullname: fullnameTextFeild.text!, email: emailTextFeild.text!, mobile: phoneTextFeild.text!, username: usernameTextFeild.text!, pin: Int(pinTextFeild.text!)!, passowrd: passwordTextFeild.text!)
````

## 2. [HIGH] Sign-up force-unwraps PIN conversion; delegate that limits input is never assigned

Location: `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` · Agents: quality

`Int(pinTextFeild.text!)!` crashes if the user enters non-numeric PIN characters. The maxLength-4 restriction in the UITextFieldDelegate extension (lines 185-192) is dead code because `textField.delegate = self` is never set for any of the form fields, so nothing constrains input to 4 digits.

Fix: Set the text field delegates in configVC, and replace the force-unwrap with `guard let pin = Int(pinTextFeild.text ?? "")` plus a validation alert.

Suggested test: Enter "abc" in the PIN field, fill the rest, tap Sign up. Expected: validation alert, not a crash.

Evidence:

````
                    let signUpResult = try await NetworkManager.shared.Signup(fullname: fullnameTextFeild.text!, email: emailTextFeild.text!, mobile: phoneTextFeild.text!, username: usernameTextFeild.text!, pin: Int(pinTextFeild.text!)!, passowrd: passwordTextFeild.text!)
````

## 3. [HIGH] Force-unwrap of amount text crashes on save (default value is "$0")

Location: `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` · Agents: tests

expensesAndIncomeTextField is initialized with textField.text = "$0" (line 43) and the user can type any characters on the numberPad. Double("$0") is nil, so the force-unwrap crashes at runtime whenever the user saves without editing the field or when parsing fails. This is a deterministic crash on the default screen state.

Fix: Parse defensively: strip non-numeric characters, use Double(text.replacingOccurrences(of: "$", with: "")) with guard/optional binding, and show a validation alert on failure instead of crashing.

Suggested test: Set expensesAndIncomeTextField.text to "$0" (the default) and invoke postTransaction(); assert no precondition failure occurs and an invalid-input alert is presented. Also test text "12.5abc".

Evidence:

````
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

## 4. [HIGH] Force-unwrap of amount text crashes on the pre-filled value "$0"

Location: `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` · Agents: quality

The amount field is initialized with text = "$0" (line 43), which is non-empty, so the Validate() empty-check passes. Double("$0") returns nil, and the trailing force-unwrap crashes the app immediately when the user taps Save without editing the amount (or types any non-numeric characters, since only .numberPad suggests—not enforces—numeric input).

Fix: Use `guard let amountText = expensesAndIncomeTextField.text, let amount = Double(amountText.replacingOccurrences(of: "$", with: ""))` and show a validation alert on failure instead of force-unwrapping.

Suggested test: Launch Add screen, leave the amount as "$0", fill other fields, tap Save. Expected: validation message, no crash.

Evidence:

````
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

## 5. [HIGH] Login request body including password logged to console

Location: `Expense Tracker/Network Manager/AuthManager.swift:39` · Agents: tests

The full LoginBody (username/email and plaintext password) is printed to the console on every login, leaking credentials into device logs and crash reports.

Fix: Remove the print or log only non-sensitive fields (e.g., that a login attempt was made).

Suggested test: Static test: assert no print statement serializes LoginBody or Pin objects.

Evidence:

````
        print("DEBUG:\(body)")
````

## 6. [HIGH] User ID trusted from local storage and embedded in API paths (IDOR-style design)

Location: `Expense Tracker/Network Manager/NetworkManager.swift:27` · Agents: security

All authenticated endpoints fetch data for a user_id taken from UserDefaults and appended into the URL. If the server does not verify the user_id against the bearer token, an attacker who can obtain/guess another user's ID can read their balance, income/expense data, and transactions, and even post transactions on their behalf (makeTransaction sends an arbitrary userID in the body at line 83).

Fix: Derive the identity server-side from the bearer token; never accept user IDs from client-controlled paths or bodies.

Suggested test: Call GET /transactions/{otherUserID} with a valid token of a different user; assert the server returns 403.

Evidence:

````
        let request = try await createRequest(with: URL(string: API.baseURL + "statements/info/\(userID ?? "N/A")"), type: .GET)
````

## 7. [MEDIUM] Forgot Password screen is non-functional — no submission, no network call

Location: `Expense Tracker/Controllers/Forget Password/ForgetPasswordVC.swift:16` · Agents: tests

ForgetPasswordVC only lays out an image and a username field. There is no submit button, no target/action, and no call to any reset-password API — the "Forget Password" button on LoginVC leads to a dead end, and the "Done" bar button only dismisses.

Fix: Add a submit action that validates the username and calls a reset endpoint via AuthManager/NetworkManager, with loading and success/error states.

Suggested test: Present ForgetPasswordVC, enter a username, tap a submit action; assert a reset request is issued and an alert is presented on both success and failure.

Evidence:

````
    let forgetuserTextFeild = ForgetPasswordTextFeild()
````

## 8. [MEDIUM] Force-unwrapped string conversions can crash the app

Location: `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` · Agents: security

Double(expensesAndIncomeTextField.text!)! crashes if the user edits the amount to non-numeric text (clearsOnBeginEditing makes intermediate states possible), and SingUpVC line 165 force-unwraps Int(pinTextFeild.text!) similarly. This is a denial-of-service/DoS via routine input.

Fix: Use safe optional conversion with a validation error path instead of force unwrapping.

Suggested test: Enter '$abc' in the amount field and tap Save; assert a validation alert appears and the app does not crash.

Evidence:

````
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

## 9. [MEDIUM] NetworkManager caches user_id at init, so requests use nil/"N/A" after login

Location: `Expense Tracker/Network Manager/NetworkManager.swift:14` · Agents: tests

`userID` is a let captured once when the NetworkManager singleton is first initialized. If the singleton is created before login completes (e.g., any early access), it will permanently read nil and every API path becomes `.../transactions/N/A`, silently failing or returning wrong-user data. It should be read dynamically on each request.

Fix: Replace the stored property with a computed property `private var userID: String? { UserDefaults.standard.string(forKey: "user_id") }` and fail fast when nil.

Suggested test: Create the singleton before setting user_id, then set user_id and call getTransaction(); assert the request URL contains the new id, not "N/A".

Evidence:

````
    private let userID          = UserDefaults.standard.string(forKey: "user_id")
````

## 10. [MEDIUM] user_id cached at singleton init, so requests use a stale/absent user id

Location: `Expense Tracker/Network Manager/NetworkManager.swift:14` · Agents: quality

NetworkManager.shared is a singleton; userID is captured when the singleton is first touched. If that happens before login (e.g., HomeVC fetch after the token write ordering differs), userID is nil and every endpoint hits "/N/A" (lines 27, 41, 54, 69), silently failing with 404. After logout/login as another user, the old id persists in memory.

Fix: Make it a computed property: `private var userID: String? { UserDefaults.standard.string(forKey: "user_id") }`, and fail fast with a typed error when nil instead of substituting "N/A".

Suggested test: Fresh install (no user_id), trigger dashboard fetch. Expected: explicit auth error handling, not a request to /statements/info/N/A.

Evidence:

````
    private let userID          = UserDefaults.standard.string(forKey: "user_id")
````

## 11. [LOW] Logout confirmation leaks loading overlay and title string-matching is fragile

Location: `Expense Tracker/Controllers/Main/ProfileVC.swift:135` · Agents: quality

showLoadingView() is called before the guard; if action.title is nil the overlay never dismisses, blocking the UI. The branch also compares display strings (`actionTitle == "logout"` / "cancel") to enum cases—an anti-pattern that silently breaks if the action titles are localized. In the 'Sign Out' path, SingOut() clears the token but not `user_id` (AuthManager.swift line 90), leaving stale identity data.

Fix: Capture the logoutOptions case in UIAlertAction and switch on it; dismiss the loading view on all paths; clear user_id in SingOut().

Suggested test: Tap Logout → choose an action. Expected: loading overlay always dismissed; after sign-out, subsequent login stores a fresh user_id.

Evidence:

````
        guard let actionTitle = action.title else { return }
````

## Review limitations

- quality: ok
  - Network layer internals (API.baseURL responses, ExError usage in other files) and derived types like Transaction extensions are outside the snapshot; some runtime behavior is inferred.
  - Constraint-conflict severity depends on runtime layout; findings about repeated constraint activation are based on code paths, not measured output.
  - LoginVC shows the loading view before validation completes (line 64) and force-unwraps validated text fields; flagged only where a concrete crash path exists.
  - Single-file evidence for Validation()/extension helpers not shown here (ValidationTextField.swift) limits assessment of regex validation usage, which appears unused by the surveyed flows.
  - Discarded unverified finding: Change Password Save button is a no-op
  - Discarded unverified finding: Header subviews and constraints re-added on every layout pass
  - Discarded unverified finding: Reused table cells keep stale Face ID switch accessory
  - Discarded unverified finding: Login error responses (4xx) throw generic invalidResponse, making the result.status!=200 branch dead and leaking debug info elsewhere
  - Discarded unverified finding: Date picker callback ignores the selected day component
  - Discarded unverified finding: Chart reconfigured and re-animated inside viewDidLayoutSubviews
  - Corrected 4 source citation(s) using unambiguous matches in the cited file; exact source excerpts retained.
- security: ok
  - Server-side implementation is not in the snapshot, so IDOR/rate-limiting severity depends on unverifiable backend behavior.
  - NetworkManager, AuthManager, and Validators are reviewed from the shown sources only; URLSession configuration (ATS, TLS pinning) and keychain alternatives not in scope.
  - Non-Swift files (Info.plist, entitlements, build settings) were not provided, so ATS exceptions and permission strings could not be verified.
  - Discarded unverified finding: Access token and user ID persisted in UserDefaults (unencrypted plist)
  - Discarded unverified finding: PIN login has no client-side attempt limiting and small keyspace
  - Discarded unverified finding: Face ID gate fails open: content stays accessible after failed authentication
  - Discarded unverified finding: Biometrics can be silently disabled without authentication
  - Discarded unverified finding: Change Password screen is non-functional (Save handler empty)
  - Discarded unverified finding: Server responses only implicitly checked; errors logged including credentials in debug output
  - Discarded unverified finding: Sign-up PIN capped at 4 chars but password/PIN validation not enforced client-side
  - Discarded unverified finding: HomeVC table cell indexing can crash on reload races
  - Corrected 2 source citation(s) using unambiguous matches in the cited file; exact source excerpts retained.
- tests: ok
  - Only the supplied snapshot was reviewed; supporting types (AuthManager.isSingedIn consumers, ExError usage, Images, DeviceTypes behavior, ProfileHeaderView.xib) were inspected statically without running the app.
  - No unit/UI test targets were present in the snapshot, so no existing coverage could be evaluated; all suggested tests are proposals.
  - Threading of UI updates inside async Task blocks (e.g., HomeVC.configData) was noted as a risk but not exhaustively verified for every call path.
  - Focus was on correctness, security, and testability of the authentication and transaction flows; layout-only nitpicks were deprioritized.
  - Discarded unverified finding: Invalid CGGradient locations force-unwrap crashes chart rendering
  - Discarded unverified finding: Biometric lock does not block access on authentication failure
  - Discarded unverified finding: Access token and user id persisted in UserDefaults
  - Discarded unverified finding: SingOut does not clear user_id and logout presents Login over existing stack
  - Discarded unverified finding: Change Password save handler is unimplemented
  - Corrected 5 source citation(s) using unambiguous matches in the cited file; exact source excerpts retained.
