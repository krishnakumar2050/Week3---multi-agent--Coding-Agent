# Code review report

Status: **complete**

Static test-gap analysis only; tests were not executed and coverage was not measured.

critical: 1 | high: 12 | medium: 14 | low: 2 | info: 0

## Aggregator synthesis

3/3 specialists succeeded; 29 verified finding(s). Highest reported severity: critical.

- [CRITICAL] `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` Force-unwrapped Double() on amount field crashes app on every transaction save: Parse the amount safely: `let cleaned = expensesAndIncomeTextField.text?.replacingOccurrences(of: "$", with: "") ?? ""` then `guard let amount = Double(cleaned) else { presentAlertOnMainThread(...); dismissLoadingView(); return }`. Also default the field to "0" instead of "$0", and add a numeric format check inside the validation step.
- [HIGH] `Expense Tracker/Controllers/Login SingUp/LoginWithPinVC.swift:170` LoginWithPinVC force-unwraps PIN text fields before validation, trapping on empty fields: Build the PIN from optional values after the validation switch, and only force-unwrap once the state is .Valid. Cover the empty-field and partial-entry cases with tests.
- [HIGH] `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` Force-unwrapped Int() on PIN field can crash sign-up: Validate the PIN with a numeric check (e.g. `guard let pin = Int(pinTextFeild.text ?? "") else { alert; return }`) and set the field's `keyboardType = .numberPad` plus `delegate = self` so the length/format rule is actually enforced.
- [HIGH] `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` SingUpVC force-unwraps Int(pinTextFeild.text!), trapping on empty or non-numeric PIN: Validate the PIN as numeric before submitting and surface a specific error message; avoid force unwrapping in the request construction.
- [HIGH] `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` AddIncomeAndExpensesVC force-unwraps a non-numeric amount, crashing on the default "$0" text: Parse the amount safely (strip non-numeric characters, use `Double(...)` optional binding) and reject invalid amounts with a validation error instead of force-unwrapping. Add unit tests covering "$0", empty, "12.50", "abc" and negative inputs.

Run: `4fe3e5e9-5292-44d4-aa2d-160f1f9d501b` · Schema: 1.0

Repository: `/Users/krishnakumar/Documents/GitHub/Expense-Tracker-App`

Snapshot SHA-256: `83ab6449ed7aab7c754f304211b83cc5e8bb9d96ec92f5933d5d63953883c24d`

Completed: 2026-11-01T10:18:59.745839+00:00 · Duration: 41.296 seconds

## Model provenance

| Agent | Requested model | Actual model | Evidence |
| --- | --- | --- | --- |
| quality | accounts/fireworks/models/minimax-m3p1-flash | accounts/fireworks/models/minimax-m3p1-flash | provider_response |
| security | accounts/fireworks/models/minimax-m3p1-flash | accounts/fireworks/models/minimax-m3p1-flash | provider_response |
| tests | accounts/fireworks/models/minimax-m3p1-flash | accounts/fireworks/models/minimax-m3p1-flash | provider_response |

## 1. [CRITICAL] Force-unwrapped Double() on amount field crashes app on every transaction save

Location: `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` · Agents: quality

The amount UITextField is pre-populated with the literal string "$0" (line 43: `textField.text = "$0"`) and `clearsOnBeginEditing = true` only clears it if the user focuses the field. The `Validate(...)` helper only checks for empty strings, so "$0" passes validation. `Double("$0")` returns nil, and the force unwrap in `Double(expensesAndIncomeTextField.text!)!` traps, crashing the app. The same happens for any non-numeric entry the numberPad cannot prevent (e.g. pasted text, or a user who never taps the field).

Fix: Parse the amount safely: `let cleaned = expensesAndIncomeTextField.text?.replacingOccurrences(of: "$", with: "") ?? ""` then `guard let amount = Double(cleaned) else { presentAlertOnMainThread(...); dismissLoadingView(); return }`. Also default the field to "0" instead of "$0", and add a numeric format check inside the validation step.

Suggested test: Open Add Income/Expenses, enter title/description/date/type but leave the amount field untouched (still "$0"), tap Save. Expected: an alert stating the amount is invalid and no crash; currently the app terminates with a force-unwrap trap.

Evidence:

````
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

## 2. [HIGH] LoginWithPinVC force-unwraps PIN text fields before validation, trapping on empty fields

Location: `Expense Tracker/Controllers/Login SingUp/LoginWithPinVC.swift:170` · Agents: tests

The PIN string is built with force unwraps before the `switch validate` block is reached. A freshly presented PIN screen has all four fields empty (text == nil for UITextField), so tapping "Go" crashes before the friendly "pin 1 cannot be Empty." validation message can ever be shown. The four-field Validate overload in UIViewController+Ext.swift (lines 57-69) is effectively unreachable through this path.

Fix: Build the PIN from optional values after the validation switch, and only force-unwrap once the state is .Valid. Cover the empty-field and partial-entry cases with tests.

Suggested test: Instantiate LoginWithPinVC, leave all PIN fields empty, trigger pinLogin(); assert no crash and that an alert with the message "pin 1 cannot be Empty." is presented. Then fill three of four fields and assert "pin 4 cannot be Empty." is shown.

Evidence:

````
        let pin = String(passInput1.text! + passInput2.text! + passInput3.text! + passInput4.text!)
````

## 3. [HIGH] Force-unwrapped Int() on PIN field can crash sign-up

Location: `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` · Agents: quality

`Int(pinTextFeild.text!)!` assumes the PIN field contains digits. The field is a plain `CustomTextFields` with the default (alphabetic) keyboard and `textContentType = .newPassword`, and the `UITextFieldDelegate` implementation of this class (line 185) is never installed on any field, so the maxLength rule is not applied either. Entering "12ab" passes the emptiness-only validation and then traps in the force unwrap.

Fix: Validate the PIN with a numeric check (e.g. `guard let pin = Int(pinTextFeild.text ?? "") else { alert; return }`) and set the field's `keyboardType = .numberPad` plus `delegate = self` so the length/format rule is actually enforced.

Suggested test: In Sign Up, enter a non-numeric PIN such as "ab" and tap Sign up. Expected: a validation alert and no crash; currently the force unwrap traps.

Evidence:

````
                    let signUpResult = try await NetworkManager.shared.Signup(fullname: fullnameTextFeild.text!, email: emailTextFeild.text!, mobile: phoneTextFeild.text!, username: usernameTextFeild.text!, pin: Int(pinTextFeild.text!)!, passowrd: passwordTextFeild.text!)
````

## 4. [HIGH] SingUpVC force-unwraps Int(pinTextFeild.text!), trapping on empty or non-numeric PIN

Location: `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` · Agents: tests

The sign-up Validate overload only checks emptiness, so a non-empty but non-numeric PIN (e.g. "12ab") reaches `Int(...)!` and traps. The delegate in this same file limits field length to 4 (line 186) but never restricts the character set, so alphabetic input is possible. No test asserts that sign-up rejects non-numeric PINs.

Fix: Validate the PIN as numeric before submitting and surface a specific error message; avoid force unwrapping in the request construction.

Suggested test: Fill the sign-up form with valid values but PIN "12ab"; assert the request is not sent and an alert mentioning an invalid PIN is presented. Repeat with a valid numeric PIN and assert Signup is called with pin == 1212.

Evidence:

````
                    let signUpResult = try await NetworkManager.shared.Signup(fullname: fullnameTextFeild.text!, email: emailTextFeild.text!, mobile: phoneTextFeild.text!, username: usernameTextFeild.text!, pin: Int(pinTextFeild.text!)!, passowrd: passwordTextFeild.text!)
````

## 5. [HIGH] AddIncomeAndExpensesVC force-unwraps a non-numeric amount, crashing on the default "$0" text

Location: `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` · Agents: tests

The amount field is pre-populated with "$0" (line 43: `textField.text = "$0"`) and uses a numberPad keyboard. Validation only checks for emptiness, so the untouched "$0" string passes Validate and reaches `Double("$0")!`, which is nil and traps. Any non-numeric residue (e.g. a locale decimal separator or a pasted value) crashes identically. There is no unit test asserting the amount parsing behavior, so this failure path is unverified.

Fix: Parse the amount safely (strip non-numeric characters, use `Double(...)` optional binding) and reject invalid amounts with a validation error instead of force-unwrapping. Add unit tests covering "$0", empty, "12.50", "abc" and negative inputs.

Suggested test: Unit test the amount parsing/validation helper: given amount text "$0" expect an invalid-state error and no network call; given "12.50" expect Double 12.5 and exactly one makeTransaction call; given "abc" expect invalid state and no crash.

Evidence:

````
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

## 6. [HIGH] TransectionsVC caches incomeTransactions in a lazy var, so the table can render with stale data

Location: `Expense Tracker/Controllers/Main/TransectionsVC.swift:69` · Agents: tests

Because `rowTransectionIndex` is a lazy stored property, it is initialized once with the value of `incomeTransactions` at first access. `getTransaction()` assigns `self.incomeTransactions` asynchronously afterwards; if the lazy property is first read before that assignment completes (which happens because viewDidLayoutSubviews reads it at line 109), it permanently holds the empty snapshot and numberOfRowsInSection returns 0. Reassigning `rowTransectionIndex = incomeTransactions` in viewDidLayoutSubviews/siutDidChange later fixes it only when a layout pass occurs after the data arrives.

Fix: Make rowTransectionIndex a computed property that derives from the current segment selection, removing the stale-snapshot class of bug entirely.

Suggested test: With a stubbed network returning 2 income and 1 expense transaction, present TransectionsVC, wait for the fetch, then force a layout pass and assert numberOfRows(inSection: 0) == 2 for the Income segment and == 1 after switching to the Expense segment.

Evidence:

````
    lazy var rowTransectionIndex = incomeTransactions
````

## 7. [HIGH] Five-field Validate overload never checks the title field

Location: `Expense Tracker/Extentions/UIViewController+Ext.swift:41` · Agents: tests

The body of this overload checks amount, type, description (the 4th parameter) and date, but never the 3rd parameter (title). An empty title therefore produces .Valid and is submitted to makeTransaction, producing transactions with an empty title. The 7-field sign-up overload does check every field, so this is an inconsistency rather than intentional behavior.

Fix: Add an explicit empty-title branch returning .InValid("Title cannot be Empty.") and add a unit test for each field being empty in turn.

Suggested test: Table-driven test over the 5 arguments of Validate(_:_:_:_:_:): for each index, leave only that field empty and assert the result is .InValid with a message naming that field; then fill all fields and assert .Valid.

Evidence:

````
    func Validate(_ amount: UITextField, _ type: UITextField, _ title: UITextField, _ description: UITextField, _ date: UITextField) -> UserValidateState {
````

## 8. [HIGH] User credentials printed to console in plaintext

Location: `Expense Tracker/Network Manager/AuthManager.swift:39` · Agents: security

The LoginBody struct contains the user's password (see Models/Login.swift:12 `let password: String`), and it is printed verbatim to the console before the request is sent. On iOS, console output is readable by any other app on a jailbroken device and is frequently captured in device syslogs/CI logs or crash reports, so the plaintext password and username leak outside the app's sandbox.

Fix: Remove the print entirely, or log only a redacted placeholder (e.g. the username with the password omitted). Never include secrets in log statements.

Suggested test: Run a login with a known password while capturing os_log/syslog output; assert the password string does not appear anywhere in the log stream.

Evidence:

````
        print("DEBUG:\(body)")
````

## 9. [HIGH] Session access token and user id stored in unencrypted UserDefaults

Location: `Expense Tracker/Network Manager/AuthManager.swift:85` · Agents: security

The bearer token returned by the server is persisted in UserDefaults, which is an unencrypted plist inside the app container. It is included in unencrypted iTunes/iCloud backups, is readable by a device with filesystem access (jailbreak, forensic image, or a malicious/compromised backup tool), and is not protected by hardware-backed storage. The bearer token alone grants full API access to the user's financial data (see NetworkManager createRequest attaching `Bearer \(token)`).

Fix: Store the access token and user id in the Keychain (kSecClassGenericPassword), ideally with `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` so it is excluded from backups, and read them on demand instead of caching them.

Suggested test: After login, assert that no value for keys "access_token" or "user_id" exists in UserDefaults.standard.dictionaryRepresentation(), and that Keychain contains the token.

Evidence:

````
        UserDefaults.standard.setValue(result.accessToken, forKey: "access_token")
        UserDefaults.standard.setValue(result.userInfo, forKey: "user_id")
````

## 10. [HIGH] NetworkManager caches user_id at singleton init, so requests use a stale/NULL user after re-login

Location: `Expense Tracker/Network Manager/NetworkManager.swift:14` · Agents: quality

`NetworkManager.shared` is a lazily created singleton whose `userID` is resolved once, at first access, and never refreshed. If the singleton is created before a login stores `user_id` (for example the first thing touched is `NetworkManager.shared.downloadImage`, or the app was created after `SingOut()` which clears only `access_token` but leaves `user_id`), every subsequent endpoint is built with `\(userID ?? "N/A")` -> `/api/v1/transactions/N/A`. Likewise, after user A logs out and user B logs in, the singleton still sends user A's id because the stored value is never re-read.

Fix: Do not cache the id in a stored property. Resolve it per request, e.g. `private var userID: String { UserDefaults.standard.string(forKey: "user_id") ?? "" }`, and throw `ExError.NotFound` from `createRequest` when it is missing. Additionally clear `user_id` in `AuthManager.SingOut()`.

Suggested test: Log in as user A, log out, log in as user B, then pull to refresh Home. Expected: the dashboard/transaction requests contain user B's id (or the app asks to sign in again if no id is present); currently the requests carry user A's id or "N/A".

Evidence:

````
    private let userID          = UserDefaults.standard.string(forKey: "user_id")
````

## 11. [HIGH] User identity cached once at singleton init, leaking data across account switches

Location: `Expense Tracker/Network Manager/NetworkManager.swift:14` · Agents: security

NetworkManager is a process-wide singleton and `userID` is resolved exactly once, when the singleton is first created. The value is never refreshed after login, logout, or an account switch. Consequence: a user who signs out and signs in with a different account will still query `/transactions/<oldUserID>`, `/statements/info/<oldUserID>` etc. with the new account's bearer token, showing one user another user's financial records (IDOR-style data disclosure), and POSTing transactions attributed to the previous account (NetworkManager.swift:83 `userID: userID!`).

Fix: Do not cache the identifier. Resolve it per request (e.g. `AuthManager.shared.currentUserID` reading Keychain/UserDefaults at call time), and fail the request if it is missing rather than substituting "N/A" for the path segment.

Suggested test: Log in as user A, load the dashboard, sign out, log in as user B, then reload the dashboard. Assert the outgoing request path contains user B's id and never user A's.

Evidence:

````
    private let userID          = UserDefaults.standard.string(forKey: "user_id")
````

## 12. [HIGH] Force unwrap of userID in makeTransaction crashes when no user id is cached

Location: `Expense Tracker/Network Manager/NetworkManager.swift:83` · Agents: quality

`userID` is optional (`UserDefaults.standard.string(forKey: "user_id")`). If it was nil when the singleton was created, `userID!` traps at runtime, crashing the app exactly when the user saves a transaction (a core flow). Other methods defensively use `userID ?? "N/A"`, so this call site is the odd one out.

Fix: Replace the force unwrap with a throwing guard, e.g. `guard let userID else { throw ExError.NotFound }`, and surface that error through the existing `catch` in `postTransaction()`.

Suggested test: Clear the `user_id` key from UserDefaults (fresh install) and attempt to save a transaction while signed out/with an empty id. Expected: an error alert ("Not Found"/sign-in required); currently the app crashes on the force unwrap.

Evidence:

````
        let request = try await createRequest(with: URL(string: API.baseURL + "transactions/usertransactions"), type: .POST, body: TransactionBody(userID: userID!, type: type, title: title, description: description, amount: amount))
````

## 13. [HIGH] NetworkManager.makeTransaction force-unwraps userID, crashing when no user is signed in

Location: `Expense Tracker/Network Manager/NetworkManager.swift:83` · Agents: tests

`userID` is a `let` initialized from UserDefaults at singleton creation (line 14) and may be nil when the app has no stored user id (fresh install, or after logout, see the SingOut finding). Other endpoints guard with `userID ?? "N/A"`, but this POST path force-unwraps and traps. No test covers posting a transaction without a stored user id.

Fix: Guard the user id and throw a typed error (e.g. ExError.NotFound) instead of force-unwrapping, matching the other endpoints.

Suggested test: With no "user_id" in UserDefaults, call makeTransaction("Expense", "t", "d", 10.0); assert it throws ExError.NotFound (or a typed auth error) and does not crash, and that no request is sent.

Evidence:

````
        let request = try await createRequest(with: URL(string: API.baseURL + "transactions/usertransactions"), type: .POST, body: TransactionBody(userID: userID!, type: type, title: title, description: description, amount: amount))
````

## 14. [MEDIUM] PIN login has no rate limiting, lockout or attempt throttling

Location: `Expense Tracker/Controllers/Login SingUp/LoginWithPinVC.swift:171` · Agents: security

The PIN is a 4-digit integer (0-9999) sent directly to `auth/pin` with no client-side throttling, no lockout counter and no delay after failed attempts. An attacker with the device (or driving the app) can enumerate all 10,000 PINs against the `auth/pin` endpoint and gain full account access, entirely bypassing the password and any rate limiting the UI might imply.

Fix: Implement server-side rate limiting/lockout for PIN attempts, and client-side progressive delays after failed attempts. Consider requiring the password (or another factor) in addition to the PIN, and monitor the endpoint for enumeration.

Suggested test: Submit repeated incorrect PINs and assert the client applies an increasing delay and/or the server rejects the account after a threshold number of attempts.

Evidence:

````
        guard let pin = Int(pin) else { return }
````

## 15. [MEDIUM] HomeVC updates UIKit from the async task without hopping to the main thread

Location: `Expense Tracker/Controllers/Main/HomeVC.swift:133` · Agents: tests

fetchDashboardData() is called from a `Task` whose executor is not guaranteed to be the main actor; configData() sets text, attributedText and triggers an image download on UIViews. On a non-main executor this is a main-thread violation (undefined behaviour / UIKit assertions), and it is not covered by any test that exercises the async path.

Fix: Mark the view controller or the fetch/configuration methods @MainActor, or wrap configData in DispatchQueue.main.async, and assert UI updates happen on the main thread.

Suggested test: In an async test, call fetchDashboardData() with a stubbed NetworkManager returning data and assert via Thread.isMainThread inside a spy on the label text setter that the configuration ran on the main thread.

Evidence:

````
            let userData = try await NetworkManager.shared.getDashboardData()
            self.profileData = userData
            configData(userData)
````

## 16. [MEDIUM] Network errors are swallowed with print(), leaving the user with stale/empty data and no feedback

Location: `Expense Tracker/Controllers/Main/HomeVC.swift:137` · Agents: quality

`fetchDashboardData()` and `fetchTransactions()` catch every error and only `print` it. When the request fails (offline, 401, decoding error), the loading view is dismissed and the screen keeps showing a zero balance, empty name and no message — the user gets no indication that loading failed. `TransectionsVC` has the same pattern (lines 141, 153, 181).

Fix: Handle the error explicitly: call `presentDefaultError()` or `presentAlertOnMainThread(...)` with the localized message and, for the empty-state, show the existing `layoutLable(...)` message so the user is told the request failed instead of seeing an empty balance.

Suggested test: Start the app with no network connectivity and open the Home tab. Expected: an error is shown to the user; currently the screen silently displays an empty/zero state.

Evidence:

````
            print(error)
````

## 17. [MEDIUM] configTableView() re-activates the same table constraints on every data fetch

Location: `Expense Tracker/Controllers/Main/HomeVC.swift:146` · Agents: quality

`fetchTransactions()` calls `configTableView()` on every successful refresh (pull-to-refresh, `refreshData`), and `configTableView()` unconditionally calls `NSLayoutConstraint.activate([...])` with the same four constraints. Each refresh therefore installs another copy of the table's constraints, causing conflicting-constraint warnings and accumulating constraints over time.

Fix: Activate the table constraints only once (guard with a `Bool` flag, or call `configTableView()` from `viewDidLoad` and keep only the data reload in the fetch path).

Suggested test: Pull to refresh the home screen 5 times and watch the console for Auto Layout conflicts / check `tableView.constraints.count` growth. Expected: constraint count stays constant; currently it grows by 4 per refresh.

Evidence:

````
                configTableView()
````

## 18. [MEDIUM] Constraint activation repeated on every layout pass in HomeVC produces duplicate/conflicting constraints

Location: `Expense Tracker/Controllers/Main/HomeVC.swift:187` · Agents: quality

`ConfigureHeaderElements()` (which ends in `NSLayoutConstraint.activate([...])` at line 244) is called from `viewWillLayoutSubviews()`, so the same ~30 constraints are activated again on every layout pass. Auto Layout then has multiple conflicting copies of the same constraint, producing "Unable to simultaneously satisfy constraints" runtime warnings and needless layout passes; `headerView.addSubViews(...)` is also re-run on each pass.

Fix: Move the one-time view construction and constraint activation into `configHomeVC()` (called from `viewDidLoad`) and remove the call from `viewWillLayoutSubviews()`. If per-layout updates are needed, keep a separate method that only mutates properties/frames, never activating constraints.

Suggested test: Open HomeVC and rotate the device or trigger repeated layout (pull to refresh). Expected: no Auto Layout constraint-conflict warnings in the console; currently constraints are duplicated on each layout pass.

Evidence:

````
        ConfigureHeaderElements()
````

## 19. [MEDIUM] Server-controlled avatar path concatenated into a URL without validation

Location: `Expense Tracker/Controllers/Main/HomeVC.swift:216` · Agents: security

The avatar field comes straight from the JSON API response (`User.avatar`) and is concatenated onto the base host without validating that it is a relative path. A value such as `../../api/v1/users/create-user` or an absolute URL-ish string can redirect the request to an unintended endpoint on the same host, and the same pattern is used in ProfileHeaderView.swift:39. `downloadImage` (NetworkManager.swift:152) then fetches and decodes whatever comes back, with no content-type or size checks, so a large or non-image response is also loaded into memory.

Fix: Validate that `avatar` is a relative path with no `..` segments and no scheme/host, build the URL with URLComponents, restrict the download to the expected host, and validate the response MIME type and size before decoding.

Suggested test: Mock the dashboard response with avatar = "../../api/v1/users/create-user" and assert the resulting request URL stays under the expected image path and no other endpoint is hit.

Evidence:

````
        userImage.downloadImage(fromURL: "https://expensetracker.abdorizak.dev/" + data.user.avatar)
````

## 20. [MEDIUM] Logout presents the login screen on top of the still-visible profile/tab stack

Location: `Expense Tracker/Controllers/Main/ProfileVC.swift:146` · Agents: quality

After `AuthManager.shared.SingOut()` the code presents a new `LoginVC` from inside `ProfileVC`, which itself is presented modally on top of `TabBarVC`. The old tab bar and profile remain in the view hierarchy underneath, so dismissing the login screen (swipe-to-dismiss on the default `.fullScreen` presentation is disabled, but any future change, or the profile's own dismissal) can reveal the logged-in app UI. Also, if `SingOut()` ever returns false, `dismissLoadingView()` is never called and the loading overlay stays on screen forever.

Fix: Dismiss the whole presenting stack before showing login: dismiss `self` (and the presenting tab bar controller) and then present `LoginVC` in the completion, or set the root view controller of the window scene to the login screen. Always call `dismissLoadingView()` in both the success and failure branches of the logout branch.

Suggested test: Log out from Profile and verify that after the login screen is dismissed no tab bar or transaction data remains accessible. Expected: the app root is the login screen; currently the authenticated UI is still in the hierarchy underneath.

Evidence:

````
                        self.present(LoginScreen, animated: true)
````

## 21. [MEDIUM] TransectionsVC activates chart constraints twice (income and expense fetch both call configChartView)

Location: `Expense Tracker/Controllers/Main/TransectionsVC.swift:139` · Agents: quality

`configChartView()` is invoked from both `fetchIncomeData()` and `fetchExpensesData()` (and again from `getTransaction()`), and each invocation calls `NSLayoutConstraint.activate([...])` for the same chartView/lineChart anchors. Duplicated constraints plus repeated `chartView.addSubview(lineChart)` calls cause Auto Layout conflict warnings and repeated chart configuration.

Fix: Call `configChartView()` once (e.g. from `viewDidLoad`) and let the fetch methods only refresh the chart data via `setChartData(...)`.

Suggested test: Open the Transactions tab and observe the console for duplicate-constraint warnings. Expected: no Auto Layout warnings and stable chart layout; currently the chart constraints are duplicated on each data fetch.

Evidence:

````
                configChartView()
````

## 22. [MEDIUM] Biometric authentication failure does not block access to app content

Location: `Expense Tracker/Custom Views/TabBar Controller/TabBarVC.swift:39` · Agents: security

When Face ID is enabled, a failed or cancelled biometric evaluation only shows a dismissible alert; the tab bar and all transaction/balance screens stay fully usable behind it. The alert's OK handler is nil, so the user can dismiss it and continue reading balances and transactions without ever authenticating. This makes the "Enable Auth" app-lock feature ineffective as an access control.

Fix: On authentication failure, block the UI (e.g. overlay a lock screen / present a blocking controller and re-prompt or sign the user out) instead of presenting a dismissible informational alert.

Suggested test: Enable Face ID, cancel the biometric prompt, and assert the transaction/balance views are not interactively accessible and a re-authentication prompt is shown.

Evidence:

````
                        if !success {
                            // Handle authentication failure
                            let alert = UIAlertController(title: "Authentication Failed", message: "Please try again.", preferredStyle: .alert)
                            alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
                            self?.present(alert, animated: true, completion: nil)
                        }
````

## 23. [MEDIUM] ProfileHeaderView re-runs commonInit() on every layout pass, duplicating constraints

Location: `Expense Tracker/Custom Views/UIView/ProfileHeaderView.swift:27` · Agents: quality

`commonInit()` loads the nib, re-adds `contentView` as a subview and re-activates the same constraints (lines 68-84). Because it is invoked from `layoutSubviews()`, this happens on every layout pass of the header, duplicating constraints and repeatedly reloading the nib, and it also overwrites `user_fullName.text` with the hard-coded "Abdorizak Abdalla Hassan" (line 60) overriding the actual user name passed to the convenience init.

Fix: Perform nib loading, subview installation and constraint activation once (guard with a `didSetup` flag or move to `init`), and remove the hard-coded name assignment so the passed-in `name` is not overwritten.

Suggested test: Open Profile and scroll the table. Expected: the header shows the signed-in user's name and no duplicate constraints are logged; currently the hard-coded name is applied and constraints are re-added on each layout.

Evidence:

````
        commonInit()
````

## 24. [MEDIUM] Sign-up Validate combined-empty check uses a comma instead of a conjunction

Location: `Expense Tracker/Extentions/UIViewController+Ext.swift:73` · Agents: tests

The condition mixes `&&` with a trailing comma expression, so the "all fields empty" message "feilds cannot be Empty" is not produced as intended (a comma expression is not a conjunction, and the confirmPass term is evaluated as a tuple rather than as part of the boolean chain). The behaviour of the all-empty branch is therefore not what the code reads like, and no test pins down the message for that case.

Fix: Use `&&` consistently across all seven fields so the combined-empty branch is reachable and deterministic.

Suggested test: Call the 7-field Validate with all seven text fields empty and assert the returned message equals "feilds cannot be Empty"; then empty only confirmPass and assert the message is "confirmPass cannot be Empty."

Evidence:

````
        if (fullname.text?.isEmpty)! && (email.text?.isEmpty)! && (mobile.text?.isEmpty)! && (username.text?.isEmpty)! && (pin.text?.isEmpty)! && (password.text?.isEmpty)!, (confirmPass.text?.isEmpty)! {
````

## 25. [MEDIUM] AuthManager turns every non-200 login response into a generic error, discarding the server message

Location: `Expense Tracker/Network Manager/AuthManager.swift:49` · Agents: tests

LoginVC (LoginVC.swift lines 70-71) and LoginWithPinVC (lines 178-179) both check `result.status != 200` and display `result.message`, but AuthManager throws before decoding whenever the HTTP status is not 200. The API therefore returns its explanatory body (e.g. "wrong password") with a non-200 status, and the user only ever sees the generic "Invalid response from the server. please try again." The intended `result.status != 200` branch is effectively dead code and no test asserts the server message is surfaced.

Fix: Decode the response body even for non-200 statuses and surface the server message (or map the status to a specific ExError such as invalidCredentials).

Suggested test: Stub a 401 response whose JSON body is {"status":401,"message":"Invalid username or password"}; assert login throws/returns an error whose message contains "Invalid username or password" rather than "Invalid response from the server".

Evidence:

````
        guard let response = response as? HTTPURLResponse, response.statusCode == 200 else { throw ExError.invalidResponse }
````

## 26. [MEDIUM] Sign out clears the token but leaves the user id and cached session data behind

Location: `Expense Tracker/Network Manager/AuthManager.swift:90` · Agents: security

SingOut removes only `access_token`; the `user_id` (stored at line 86) and the `isFaceIDEnabled` flag remain, and the NSCache of downloaded avatars in NetworkManager is never invalidated. On the next launch `AuthManager.shared.isSingedIn` correctly evaluates to false, but the stale `user_id` is still used as the path parameter for every transaction/statement request, and cached avatar images of the previous user can still be rendered. This compounds the stale-identity issue in NetworkManager.swift:14 and can expose the previous user's data on a shared device.

Fix: On sign out, remove `user_id` as well, clear any cached user-specific images/data, and invalidate the NetworkManager image cache.

Suggested test: Sign in as user A, sign out, then assert UserDefaults contains no "access_token" or "user_id", and that the image cache no longer holds user A's avatar.

Evidence:

````
        UserDefaults.standard.setValue(nil, forKey: "access_token")
        return true
````

## 27. [MEDIUM] NetworkManager captures userID once at singleton init, so it goes stale after login/logout

Location: `Expense Tracker/Network Manager/NetworkManager.swift:14` · Agents: tests

This is evaluated when NetworkManager.shared is first created. AuthManager.catchToken writes "user_id" to UserDefaults only during login (AuthManager.swift line 86), and SingOut clears "access_token" but never "user_id". Consequently the singleton can hold nil (requests go to .../statements/info/N/A) or a previous user's id (data of the previous account is fetched after re-login). No test exercises a login → fetch → logout → login sequence.

Fix: Resolve the user id lazily per request (read UserDefaults inside each method) and clear "user_id" in SingOut.

Suggested test: Set "user_id" to "u1", then to "u2", and assert each generated request URL contains the id that is current at call time; after AuthManager.shared.SingOut(), assert "user_id" is cleared from UserDefaults.

Evidence:

````
    private let userID          = UserDefaults.standard.string(forKey: "user_id")
````

## 28. [LOW] Biometric app-lock state stored in user-writable UserDefaults

Location: `Expense Tracker/Controllers/Main/ProfileVC.swift:204` · Agents: security

The "isFaceIDEnabled" flag that gates the Face ID lock (read in TabBarVC.swift:27) is stored in UserDefaults, which is plain user-writable storage and is restored from unencrypted backups. A user (or anyone restoring a modified backup) can flip the flag to disable the biometric lock without an authentication step; the disabling path also performs no biometric verification, unlike the enabling path.

Fix: Treat the lock flag as a security setting and store it in the Keychain (or require biometric verification before allowing it to be turned off), and re-authenticate before disabling the lock.

Suggested test: Attempt to disable the Face ID toggle and assert that a biometric or device-passcode verification is required before the flag changes.

Evidence:

````
            UserDefaults.standard.set(false, forKey: "isFaceIDEnabled")
````

## 29. [LOW] Force unwraps on server-provided and user-provided values can crash the app

Location: `Expense Tracker/Network Manager/NetworkManager.swift:83` · Agents: security

`userID!` is force-unwrapped. Because `userID` is nil whenever the app has not completed a login (or after the id has been cleared), posting a transaction crashes the app with a fatal error instead of surfacing an auth error. The same pattern appears in SingUpVC.swift:165 (`Int(pinTextFeild.text!)!`) and in HomeVC/TransectionsVC where `text!` is used on optional text-field contents, all of which are reachable from user input.

Fix: Replace force unwraps with throwing/guarded handling: throw ExError.NotFound when the user id is missing and return an explicit validation error for non-numeric input, so an unauthenticated or malformed request fails gracefully instead of terminating the process.

Suggested test: Clear the stored user id, attempt to save a transaction, and assert an error alert is shown and the app does not terminate.

Evidence:

````
        let request = try await createRequest(with: URL(string: API.baseURL + "transactions/usertransactions"), type: .POST, body: TransactionBody(userID: userID!, type: type, title: title, description: description, amount: amount))
````

## Review limitations

- quality: ok
  - Only the supplied snapshot was reviewed; helpers such as `NetworkManager` internals of the backend, `DataLoadingVC` base-class usage and `MockData` were partially visible.
  - The implementation of `Validate(...)` overloads and `ExError` usage was inferred from call sites; `Validation.validateName/validatePhoneNumber/...` helpers exist but appear unused by the reviewed screens.
  - Layout-warning findings (duplicate constraints) are based on static reading of `NSLayoutConstraint.activate` call sites; exact runtime warning text could not be observed without executing the app.
  - Behaviour of `AuthManager.SingOut()` returning false was not observed (it currently always returns true), so that part of the logout finding is defensive rather than confirmed.
- security: ok
  - The network layer implementation behind the API endpoints (auth/pin, auth/login, transaction authorization) is server-side and not present in this snapshot, so client-side findings about brute force, IDOR and authorization can only be confirmed from the client behaviour and cannot be validated against server enforcement.
  - The FileManager-based storage of the token in UserDefaults was assessed from source only; no runtime/backup inspection was performed.
  - No dependency manifests (Package.swift / Podfile) were included in the snapshot, so no insecure third-party dependency assessment could be made.
  - Hardcoded API base URL uses HTTPS, but no certificate pinning was found; this was noted but not raised as a standalone finding since the API host is a first-party domain.
  - Discarded unverified finding: Change-password and forget-password features are inert, giving a false sense of credential control
- tests: ok
  - No test files were included in the snapshot, so coverage of the described behaviors could not be observed directly; all findings are static-analysis based and expressed as recommended test scenarios.
  - Types not present in the snapshot (Validate's exact overload resolution for 5 vs 7 arguments, AuthManager/NetworkManager stubs, MockData image assets, DeviceTypes branches) were inferred from call sites.
  - The Swift comma-expression in the 7-field Validate overload may in fact be a compile-time error rather than a runtime misbehavior; this could not be verified without a compiler.
  - Network responses and API error semantics are not observable from the snapshot, so the exact status/message combination returned by the backend is assumed.
