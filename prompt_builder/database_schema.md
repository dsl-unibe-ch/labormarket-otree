# Database Schema

**Database:** `db.sqlite3`  
**Generated:** 2026-01-09 17:30:57  
**Total Tables:** 22

## Table of Contents

- [intro_quiz_group](#intro-quiz-group)
- [intro_quiz_player](#intro-quiz-player)
- [intro_quiz_subsession](#intro-quiz-subsession)
- [labor_market_companylabels](#labor-market-companylabels)
- [labor_market_employeelabels](#labor-market-employeelabels)
- [labor_market_group](#labor-market-group)
- [labor_market_offer](#labor-market-offer)
- [labor_market_player](#labor-market-player)
- [labor_market_subsession](#labor-market-subsession)
- [otree_chatmessage](#otree-chatmessage)
- [otree_completedgbatwaitpage](#otree-completedgbatwaitpage)
- [otree_completedgroupwaitpage](#otree-completedgroupwaitpage)
- [otree_completedsubsessionwaitpage](#otree-completedsubsessionwaitpage)
- [otree_pagetimebatch](#otree-pagetimebatch)
- [otree_participant](#otree-participant)
- [otree_participantvarsfromrest](#otree-participantvarsfromrest)
- [otree_roomtosession](#otree-roomtosession)
- [otree_session](#otree-session)
- [otree_taskqueuemessage](#otree-taskqueuemessage)
- [outro_quiz_group](#outro-quiz-group)
- [outro_quiz_player](#outro-quiz-player)
- [outro_quiz_subsession](#outro-quiz-subsession)

---

## intro_quiz_group

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `id_in_subsession` | INTEGER | ✅ | - | - |
| `round_number` | INTEGER | ✅ | - | - |
| `subsession_id` | INTEGER | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 0

### CREATE Statement

```sql
CREATE TABLE intro_quiz_group (
	id INTEGER NOT NULL, 
	id_in_subsession INTEGER, 
	round_number INTEGER, 
	subsession_id INTEGER, 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(subsession_id) REFERENCES intro_quiz_subsession (id) ON DELETE CASCADE, 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

## intro_quiz_player

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `id_in_group` | INTEGER | ✅ | - | - |
| `_payoff` | TEXT | ✅ | - | - |
| `round_number` | INTEGER | ✅ | - | - |
| `_role` | VARCHAR | ❌ | - | - |
| `label` | VARCHAR(10000) | ✅ | - | - |
| `skill` | INTEGER | ✅ | - | - |
| `response` | INTEGER | ✅ | - | - |
| `is_correct` | BOOLEAN | ✅ | - | - |
| `subsession_id` | INTEGER | ✅ | - | - |
| `group_id` | INTEGER | ✅ | - | - |
| `participant_id` | INTEGER | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 0

### CREATE Statement

```sql
CREATE TABLE intro_quiz_player (
	id INTEGER NOT NULL, 
	id_in_group INTEGER, 
	_payoff TEXT, 
	round_number INTEGER, 
	_role VARCHAR NOT NULL, 
	label VARCHAR(10000), 
	skill INTEGER, 
	response INTEGER, 
	is_correct BOOLEAN, 
	subsession_id INTEGER, 
	group_id INTEGER, 
	participant_id INTEGER, 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	CHECK (is_correct IN (0, 1)), 
	FOREIGN KEY(subsession_id) REFERENCES intro_quiz_subsession (id) ON DELETE CASCADE, 
	FOREIGN KEY(group_id) REFERENCES intro_quiz_group (id), 
	FOREIGN KEY(participant_id) REFERENCES otree_participant (id), 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

## intro_quiz_subsession

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `round_number` | INTEGER | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 0

### CREATE Statement

```sql
CREATE TABLE intro_quiz_subsession (
	id INTEGER NOT NULL, 
	round_number INTEGER, 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

## labor_market_companylabels

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `name` | VARCHAR(10000) | ✅ | - | - |

**Total Rows:** 0

### CREATE Statement

```sql
CREATE TABLE labor_market_companylabels (
	id INTEGER NOT NULL, 
	name VARCHAR(10000), 
	PRIMARY KEY (id)
)
```

---

## labor_market_employeelabels

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `name` | VARCHAR(10000) | ✅ | - | - |

**Total Rows:** 0

### CREATE Statement

```sql
CREATE TABLE labor_market_employeelabels (
	id INTEGER NOT NULL, 
	name VARCHAR(10000), 
	PRIMARY KEY (id)
)
```

---

## labor_market_group

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `id_in_subsession` | INTEGER | ✅ | - | - |
| `round_number` | INTEGER | ✅ | - | - |
| `subsession_id` | INTEGER | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 20

### CREATE Statement

```sql
CREATE TABLE labor_market_group (
	id INTEGER NOT NULL, 
	id_in_subsession INTEGER, 
	round_number INTEGER, 
	subsession_id INTEGER, 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(subsession_id) REFERENCES labor_market_subsession (id) ON DELETE CASCADE, 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

## labor_market_offer

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `period` | INTEGER | ✅ | - | - |
| `step` | INTEGER | ✅ | - | - |
| `wage` | TEXT | ✅ | - | - |
| `training` | BOOLEAN | ✅ | - | - |
| `accepted` | BOOLEAN | ✅ | - | - |
| `rejected` | BOOLEAN | ✅ | - | - |
| `effort` | INTEGER | ✅ | - | - |
| `revenue` | TEXT | ✅ | - | - |
| `manager_id` | INTEGER | ✅ | - | - |
| `employee_id` | INTEGER | ✅ | - | - |
| `group_id` | INTEGER | ✅ | - | - |

**Total Rows:** 6

### CREATE Statement

```sql
CREATE TABLE labor_market_offer (
	id INTEGER NOT NULL, 
	period INTEGER, 
	step INTEGER, 
	wage TEXT, 
	training BOOLEAN, 
	accepted BOOLEAN, 
	rejected BOOLEAN, 
	effort INTEGER, 
	revenue TEXT, 
	manager_id INTEGER, 
	employee_id INTEGER, 
	group_id INTEGER, 
	PRIMARY KEY (id), 
	CHECK (training IN (0, 1)), 
	CHECK (accepted IN (0, 1)), 
	CHECK (rejected IN (0, 1)), 
	FOREIGN KEY(manager_id) REFERENCES labor_market_player (id) ON DELETE CASCADE, 
	FOREIGN KEY(employee_id) REFERENCES labor_market_player (id) ON DELETE CASCADE, 
	FOREIGN KEY(group_id) REFERENCES labor_market_group (id) ON DELETE CASCADE
)
```

---

## labor_market_player

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `id_in_group` | INTEGER | ✅ | - | - |
| `_payoff` | TEXT | ✅ | - | - |
| `round_number` | INTEGER | ✅ | - | - |
| `_role` | VARCHAR | ❌ | - | - |
| `label` | VARCHAR(10000) | ✅ | - | - |
| `skill` | INTEGER | ✅ | - | - |
| `skill_increase` | BOOLEAN | ✅ | - | - |
| `offer_step` | INTEGER | ✅ | - | - |
| `payoff_calculated` | BOOLEAN | ✅ | - | - |
| `offer_employee` | INTEGER | ✅ | - | - |
| `offer_wage` | TEXT | ✅ | - | - |
| `offer_training` | BOOLEAN | ✅ | - | - |
| `offer_none` | BOOLEAN | ✅ | - | - |
| `player_matched` | INTEGER | ✅ | - | - |
| `work_effort` | INTEGER | ✅ | - | - |
| `subsession_id` | INTEGER | ✅ | - | - |
| `group_id` | INTEGER | ✅ | - | - |
| `participant_id` | INTEGER | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 240

### CREATE Statement

```sql
CREATE TABLE labor_market_player (
	id INTEGER NOT NULL, 
	id_in_group INTEGER, 
	_payoff TEXT, 
	round_number INTEGER, 
	_role VARCHAR NOT NULL, 
	label VARCHAR(10000), 
	skill INTEGER, 
	skill_increase BOOLEAN, 
	offer_step INTEGER, 
	payoff_calculated BOOLEAN, 
	offer_employee INTEGER, 
	offer_wage TEXT, 
	offer_training BOOLEAN, 
	offer_none BOOLEAN, 
	player_matched INTEGER, 
	work_effort INTEGER, 
	subsession_id INTEGER, 
	group_id INTEGER, 
	participant_id INTEGER, 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	CHECK (skill_increase IN (0, 1)), 
	CHECK (payoff_calculated IN (0, 1)), 
	CHECK (offer_training IN (0, 1)), 
	CHECK (offer_none IN (0, 1)), 
	FOREIGN KEY(subsession_id) REFERENCES labor_market_subsession (id) ON DELETE CASCADE, 
	FOREIGN KEY(group_id) REFERENCES labor_market_group (id), 
	FOREIGN KEY(participant_id) REFERENCES otree_participant (id), 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

## labor_market_subsession

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `round_number` | INTEGER | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 20

### CREATE Statement

```sql
CREATE TABLE labor_market_subsession (
	id INTEGER NOT NULL, 
	round_number INTEGER, 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

## otree_chatmessage

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `channel` | VARCHAR(255) | ✅ | - | - |
| `participant_id` | INTEGER | ✅ | - | - |
| `nickname` | VARCHAR(255) | ✅ | - | - |
| `body` | TEXT | ✅ | - | - |
| `timestamp` | FLOAT | ✅ | - | - |

**Total Rows:** 0

### CREATE Statement

```sql
CREATE TABLE otree_chatmessage (
	id INTEGER NOT NULL, 
	channel VARCHAR(255), 
	participant_id INTEGER, 
	nickname VARCHAR(255), 
	body TEXT, 
	timestamp FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(participant_id) REFERENCES otree_participant (id) ON DELETE CASCADE
)
```

---

## otree_completedgbatwaitpage

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `page_index` | INTEGER | ✅ | - | - |
| `id_in_subsession` | INTEGER | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 0

### CREATE Statement

```sql
CREATE TABLE otree_completedgbatwaitpage (
	id INTEGER NOT NULL, 
	page_index INTEGER, 
	id_in_subsession INTEGER, 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

## otree_completedgroupwaitpage

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `page_index` | INTEGER | ✅ | - | - |
| `group_id` | INTEGER | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 3

### CREATE Statement

```sql
CREATE TABLE otree_completedgroupwaitpage (
	id INTEGER NOT NULL, 
	page_index INTEGER, 
	group_id INTEGER, 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

## otree_completedsubsessionwaitpage

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `page_index` | INTEGER | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 0

### CREATE Statement

```sql
CREATE TABLE otree_completedsubsessionwaitpage (
	id INTEGER NOT NULL, 
	page_index INTEGER, 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

## otree_pagetimebatch

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `text` | TEXT | ✅ | - | - |

**Total Rows:** 3

### CREATE Statement

```sql
CREATE TABLE otree_pagetimebatch (
	id INTEGER NOT NULL, 
	text TEXT, 
	PRIMARY KEY (id)
)
```

---

## otree_participant

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `_vars` | TEXT | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |
| `label` | VARCHAR(100) | ✅ | - | - |
| `id_in_session` | INTEGER | ✅ | - | - |
| `payoff` | TEXT | ✅ | - | - |
| `time_started_utc` | VARCHAR(50) | ✅ | - | - |
| `mturk_assignment_id` | VARCHAR(50) | ✅ | - | - |
| `mturk_worker_id` | VARCHAR(50) | ✅ | - | - |
| `_index_in_pages` | INTEGER | ✅ | - | - |
| `_monitor_note` | VARCHAR(300) | ✅ | - | - |
| `code` | VARCHAR(16) | ❌ | - | - |
| `_session_code` | VARCHAR(16) | ✅ | - | - |
| `visited` | BOOLEAN | ✅ | - | - |
| `_last_page_timestamp` | INTEGER | ✅ | - | - |
| `_last_request_timestamp` | INTEGER | ✅ | - | - |
| `is_on_wait_page` | BOOLEAN | ✅ | - | - |
| `_current_page_name` | VARCHAR(200) | ✅ | - | - |
| `_current_app_name` | VARCHAR(200) | ✅ | - | - |
| `_round_number` | INTEGER | ✅ | - | - |
| `_current_form_page_url` | VARCHAR(500) | ✅ | - | - |
| `_max_page_index` | INTEGER | ✅ | - | - |
| `_is_bot` | BOOLEAN | ✅ | - | - |
| `is_browser_bot` | BOOLEAN | ✅ | - | - |
| `_timeout_expiration_time` | FLOAT | ✅ | - | - |
| `_timeout_page_index` | INTEGER | ✅ | - | - |
| `_gbat_is_connected` | BOOLEAN | ✅ | - | - |
| `_gbat_tab_hidden` | BOOLEAN | ✅ | - | - |
| `_gbat_page_index` | INTEGER | ✅ | - | - |
| `_gbat_grouped` | BOOLEAN | ✅ | - | - |

**Total Rows:** 24

### CREATE Statement

```sql
CREATE TABLE otree_participant (
	id INTEGER NOT NULL, 
	_vars TEXT, 
	session_id INTEGER, 
	label VARCHAR(100), 
	id_in_session INTEGER, 
	payoff TEXT, 
	time_started_utc VARCHAR(50), 
	mturk_assignment_id VARCHAR(50), 
	mturk_worker_id VARCHAR(50), 
	_index_in_pages INTEGER, 
	_monitor_note VARCHAR(300), 
	code VARCHAR(16) NOT NULL, 
	_session_code VARCHAR(16), 
	visited BOOLEAN, 
	_last_page_timestamp INTEGER, 
	_last_request_timestamp INTEGER, 
	is_on_wait_page BOOLEAN, 
	_current_page_name VARCHAR(200), 
	_current_app_name VARCHAR(200), 
	_round_number INTEGER, 
	_current_form_page_url VARCHAR(500), 
	_max_page_index INTEGER, 
	_is_bot BOOLEAN, 
	is_browser_bot BOOLEAN, 
	_timeout_expiration_time FLOAT, 
	_timeout_page_index INTEGER, 
	_gbat_is_connected BOOLEAN, 
	_gbat_tab_hidden BOOLEAN, 
	_gbat_page_index INTEGER, 
	_gbat_grouped BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE, 
	CHECK (visited IN (0, 1)), 
	CHECK (is_on_wait_page IN (0, 1)), 
	CHECK (_is_bot IN (0, 1)), 
	CHECK (is_browser_bot IN (0, 1)), 
	CHECK (_gbat_is_connected IN (0, 1)), 
	CHECK (_gbat_tab_hidden IN (0, 1)), 
	CHECK (_gbat_grouped IN (0, 1))
)
```

---

## otree_participantvarsfromrest

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `participant_label` | VARCHAR(255) | ✅ | - | - |
| `room_name` | VARCHAR(255) | ✅ | - | - |
| `_json_data` | TEXT | ✅ | - | - |

**Total Rows:** 0

### CREATE Statement

```sql
CREATE TABLE otree_participantvarsfromrest (
	id INTEGER NOT NULL, 
	participant_label VARCHAR(255), 
	room_name VARCHAR(255), 
	_json_data TEXT, 
	PRIMARY KEY (id)
)
```

---

## otree_roomtosession

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `room_name` | VARCHAR(255) | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 0

### CREATE Statement

```sql
CREATE TABLE otree_roomtosession (
	id INTEGER NOT NULL, 
	room_name VARCHAR(255), 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (room_name), 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

## otree_session

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `_vars` | TEXT | ✅ | - | - |
| `config` | TEXT | ✅ | - | - |
| `label` | VARCHAR | ✅ | - | - |
| `code` | VARCHAR(16) | ❌ | - | - |
| `mturk_HITId` | VARCHAR(300) | ✅ | - | - |
| `mturk_HITGroupId` | VARCHAR(300) | ✅ | - | - |
| `is_mturk` | BOOLEAN | ✅ | - | - |
| `mturk_use_sandbox` | BOOLEAN | ✅ | - | - |
| `mturk_expiration` | FLOAT | ✅ | - | - |
| `mturk_qual_id` | VARCHAR(50) | ✅ | - | - |
| `archived` | BOOLEAN | ✅ | - | - |
| `comment` | TEXT | ✅ | - | - |
| `_anonymous_code` | VARCHAR(20) | ❌ | - | - |
| `is_demo` | BOOLEAN | ✅ | - | - |
| `_admin_report_app_names` | TEXT | ✅ | - | - |
| `_admin_report_num_rounds` | VARCHAR(255) | ✅ | - | - |
| `num_participants` | INTEGER | ✅ | - | - |
| `_created` | INTEGER | ✅ | - | - |

**Total Rows:** 2

### CREATE Statement

```sql
CREATE TABLE otree_session (
	id INTEGER NOT NULL, 
	_vars TEXT, 
	config TEXT, 
	label VARCHAR, 
	code VARCHAR(16) NOT NULL, 
	"mturk_HITId" VARCHAR(300), 
	"mturk_HITGroupId" VARCHAR(300), 
	is_mturk BOOLEAN, 
	mturk_use_sandbox BOOLEAN, 
	mturk_expiration FLOAT, 
	mturk_qual_id VARCHAR(50), 
	archived BOOLEAN, 
	comment TEXT, 
	_anonymous_code VARCHAR(20) NOT NULL, 
	is_demo BOOLEAN, 
	_admin_report_app_names TEXT, 
	_admin_report_num_rounds VARCHAR(255), 
	num_participants INTEGER, 
	_created INTEGER, 
	PRIMARY KEY (id), 
	CHECK (is_mturk IN (0, 1)), 
	CHECK (mturk_use_sandbox IN (0, 1)), 
	CHECK (archived IN (0, 1)), 
	CHECK (is_demo IN (0, 1))
)
```

---

## otree_taskqueuemessage

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `method` | VARCHAR(50) | ✅ | - | - |
| `kwargs_json` | TEXT | ✅ | - | - |
| `epoch_time` | INTEGER | ✅ | - | - |

**Total Rows:** 0

### CREATE Statement

```sql
CREATE TABLE otree_taskqueuemessage (
	id INTEGER NOT NULL, 
	method VARCHAR(50), 
	kwargs_json TEXT, 
	epoch_time INTEGER, 
	PRIMARY KEY (id)
)
```

---

## outro_quiz_group

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `id_in_subsession` | INTEGER | ✅ | - | - |
| `round_number` | INTEGER | ✅ | - | - |
| `subsession_id` | INTEGER | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 2

### CREATE Statement

```sql
CREATE TABLE outro_quiz_group (
	id INTEGER NOT NULL, 
	id_in_subsession INTEGER, 
	round_number INTEGER, 
	subsession_id INTEGER, 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(subsession_id) REFERENCES outro_quiz_subsession (id) ON DELETE CASCADE, 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

## outro_quiz_player

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `id_in_group` | INTEGER | ✅ | - | - |
| `_payoff` | TEXT | ✅ | - | - |
| `round_number` | INTEGER | ✅ | - | - |
| `_role` | VARCHAR | ❌ | - | - |
| `e_peq_quiz1` | INTEGER | ✅ | - | - |
| `e_peq_quiz2` | INTEGER | ✅ | - | - |
| `e_peq_quiz3` | INTEGER | ✅ | - | - |
| `e_peq_quiz4` | INTEGER | ✅ | - | - |
| `e_peq_quiz5` | INTEGER | ✅ | - | - |
| `e_peq_quiz6` | INTEGER | ✅ | - | - |
| `e_peq_quiz7` | INTEGER | ✅ | - | - |
| `e_peq_quiz8` | INTEGER | ✅ | - | - |
| `e_peq_quiz9` | INTEGER | ✅ | - | - |
| `e_peq_quiz10` | INTEGER | ✅ | - | - |
| `e_peq_quiz11` | INTEGER | ✅ | - | - |
| `e_peq_quiz12` | INTEGER | ✅ | - | - |
| `e_peq_quiz13` | INTEGER | ✅ | - | - |
| `e_peq_quiz14` | INTEGER | ✅ | - | - |
| `e_peq_quiz15` | INTEGER | ✅ | - | - |
| `e_peq_quiz16` | INTEGER | ✅ | - | - |
| `e_peq_quiz17` | INTEGER | ✅ | - | - |
| `m_peq_quiz1` | INTEGER | ✅ | - | - |
| `m_peq_quiz2` | INTEGER | ✅ | - | - |
| `m_peq_quiz3` | INTEGER | ✅ | - | - |
| `m_peq_quiz4` | INTEGER | ✅ | - | - |
| `m_peq_quiz5` | INTEGER | ✅ | - | - |
| `m_peq_quiz6` | INTEGER | ✅ | - | - |
| `m_peq_quiz7` | INTEGER | ✅ | - | - |
| `m_peq_quiz8` | INTEGER | ✅ | - | - |
| `m_peq_quiz9` | INTEGER | ✅ | - | - |
| `m_peq_quiz10` | INTEGER | ✅ | - | - |
| `m_peq_quiz11` | INTEGER | ✅ | - | - |
| `m_peq_quiz12` | INTEGER | ✅ | - | - |
| `m_peq_quiz13` | INTEGER | ✅ | - | - |
| `m_peq_quiz14` | INTEGER | ✅ | - | - |
| `m_peq_quiz15` | INTEGER | ✅ | - | - |
| `m_peq_quiz16` | INTEGER | ✅ | - | - |
| `m_peq_quiz17` | INTEGER | ✅ | - | - |
| `demographic_quiz1` | VARCHAR(10000) | ✅ | - | - |
| `demographic_quiz2` | INTEGER | ✅ | - | - |
| `demographic_quiz3` | VARCHAR(10000) | ✅ | - | - |
| `demographic_quiz4` | VARCHAR(50) | ✅ | - | - |
| `demographic_quiz5` | FLOAT | ✅ | - | - |
| `demographic_quiz6` | INTEGER | ✅ | - | - |
| `demographic_quiz7` | INTEGER | ✅ | - | - |
| `demographic_quiz8` | TEXT | ✅ | - | - |
| `skill` | INTEGER | ✅ | - | - |
| `response` | INTEGER | ✅ | - | - |
| `is_correct` | BOOLEAN | ✅ | - | - |
| `subsession_id` | INTEGER | ✅ | - | - |
| `group_id` | INTEGER | ✅ | - | - |
| `participant_id` | INTEGER | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 24

### CREATE Statement

```sql
CREATE TABLE outro_quiz_player (
	id INTEGER NOT NULL, 
	id_in_group INTEGER, 
	_payoff TEXT, 
	round_number INTEGER, 
	_role VARCHAR NOT NULL, 
	e_peq_quiz1 INTEGER, 
	e_peq_quiz2 INTEGER, 
	e_peq_quiz3 INTEGER, 
	e_peq_quiz4 INTEGER, 
	e_peq_quiz5 INTEGER, 
	e_peq_quiz6 INTEGER, 
	e_peq_quiz7 INTEGER, 
	e_peq_quiz8 INTEGER, 
	e_peq_quiz9 INTEGER, 
	e_peq_quiz10 INTEGER, 
	e_peq_quiz11 INTEGER, 
	e_peq_quiz12 INTEGER, 
	e_peq_quiz13 INTEGER, 
	e_peq_quiz14 INTEGER, 
	e_peq_quiz15 INTEGER, 
	e_peq_quiz16 INTEGER, 
	e_peq_quiz17 INTEGER, 
	m_peq_quiz1 INTEGER, 
	m_peq_quiz2 INTEGER, 
	m_peq_quiz3 INTEGER, 
	m_peq_quiz4 INTEGER, 
	m_peq_quiz5 INTEGER, 
	m_peq_quiz6 INTEGER, 
	m_peq_quiz7 INTEGER, 
	m_peq_quiz8 INTEGER, 
	m_peq_quiz9 INTEGER, 
	m_peq_quiz10 INTEGER, 
	m_peq_quiz11 INTEGER, 
	m_peq_quiz12 INTEGER, 
	m_peq_quiz13 INTEGER, 
	m_peq_quiz14 INTEGER, 
	m_peq_quiz15 INTEGER, 
	m_peq_quiz16 INTEGER, 
	m_peq_quiz17 INTEGER, 
	demographic_quiz1 VARCHAR(10000), 
	demographic_quiz2 INTEGER, 
	demographic_quiz3 VARCHAR(10000), 
	demographic_quiz4 VARCHAR(50), 
	demographic_quiz5 FLOAT, 
	demographic_quiz6 INTEGER, 
	demographic_quiz7 INTEGER, 
	demographic_quiz8 TEXT, 
	skill INTEGER, 
	response INTEGER, 
	is_correct BOOLEAN, 
	subsession_id INTEGER, 
	group_id INTEGER, 
	participant_id INTEGER, 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	CHECK (is_correct IN (0, 1)), 
	FOREIGN KEY(subsession_id) REFERENCES outro_quiz_subsession (id) ON DELETE CASCADE, 
	FOREIGN KEY(group_id) REFERENCES outro_quiz_group (id), 
	FOREIGN KEY(participant_id) REFERENCES otree_participant (id), 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

## outro_quiz_subsession

| Column Name | Type | Nullable | Default | Primary Key |
|-------------|------|----------|---------|-------------|
| `id` | INTEGER | ❌ | - | 🔑 |
| `round_number` | INTEGER | ✅ | - | - |
| `session_id` | INTEGER | ✅ | - | - |

**Total Rows:** 2

### CREATE Statement

```sql
CREATE TABLE outro_quiz_subsession (
	id INTEGER NOT NULL, 
	round_number INTEGER, 
	session_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(session_id) REFERENCES otree_session (id) ON DELETE CASCADE
)
```

---

