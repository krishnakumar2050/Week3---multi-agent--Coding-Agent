# Expense Tracker: Fireworks model comparison

All runs used the same 64-file Swift snapshot, three parallel specialists, the same prompts, and deterministic aggregation. External knowledge enrichment was disabled for all runs.

| Model | Status | Findings | Critical | High | Medium | Low | Info | Seconds |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| minimax-m3p1-flash | complete | 29 | 1 | 12 | 14 | 2 | 0 | 41.3 |
| glm-5p3-flash | complete | 11 | 0 | 6 | 4 | 1 | 0 | 25.0 |
| glm-5p3 | complete | 26 | 0 | 10 | 10 | 5 | 1 | 37.0 |

Snapshot SHA-256: `83ab6449ed7aab7c754f304211b83cc5e8bb9d96ec92f5933d5d63953883c24d`

All nine specialist calls succeeded. Requested model IDs matched provider-reported model IDs. Findings have verified source excerpts; reasoning and severity have not been independently validated. Counts can include differently titled reports of the same issue, and higher counts do not establish better accuracy. Tests were not executed. This is one run per model, not a quality benchmark.

Previous Codex run: 24 findings; same snapshot: True.

## minimax-m3p1-flash

[Full Markdown report](minimax-m3p1-flash.md) · [JSON](minimax-m3p1-flash.json)

- [CRITICAL] Force-unwrapped Double() on amount field crashes app on every transaction save — `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237`
- [HIGH] LoginWithPinVC force-unwraps PIN text fields before validation, trapping on empty fields — `Expense Tracker/Controllers/Login SingUp/LoginWithPinVC.swift:170`
- [HIGH] Force-unwrapped Int() on PIN field can crash sign-up — `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165`
- [HIGH] SingUpVC force-unwraps Int(pinTextFeild.text!), trapping on empty or non-numeric PIN — `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165`
- [HIGH] AddIncomeAndExpensesVC force-unwraps a non-numeric amount, crashing on the default "$0" text — `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237`

## glm-5p3-flash

[Full Markdown report](glm-5p3-flash.md) · [JSON](glm-5p3-flash.json)

- [HIGH] PIN signup force-unwrap crashes; delegate limiting input is never attached — `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165`
- [HIGH] Sign-up force-unwraps PIN conversion; delegate that limits input is never assigned — `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165`
- [HIGH] Force-unwrap of amount text crashes on save (default value is "$0") — `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237`
- [HIGH] Force-unwrap of amount text crashes on the pre-filled value "$0" — `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237`
- [HIGH] Login request body including password logged to console — `Expense Tracker/Network Manager/AuthManager.swift:39`

## glm-5p3

[Full Markdown report](glm-5p3.md) · [JSON](glm-5p3.json)

- [HIGH] Account access via 4-digit PIN with no rate limiting or lockout — `Expense Tracker/Controllers/Login SingUp/LoginWithPinVC.swift:177`
- [HIGH] Force unwrap crash on invalid PIN during sign-up — `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165`
- [HIGH] Force unwrap of non-numeric PIN crashes sign-up — `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165`
- [HIGH] 4-character limit applied to every signup field via shared UITextFieldDelegate — `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:185`
- [HIGH] Force unwrap crash on non-numeric amount in postTransaction — `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237`
