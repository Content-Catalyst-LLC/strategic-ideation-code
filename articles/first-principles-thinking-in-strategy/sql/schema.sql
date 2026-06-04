PRAGMA foreign_keys = ON;
DROP VIEW IF EXISTS first_principles_profile_scores;
DROP VIEW IF EXISTS assumption_burden_register;
DROP VIEW IF EXISTS reconstructed_option_scores;
DROP TABLE IF EXISTS strategy_contexts;
CREATE TABLE strategy_contexts (
    context_id TEXT PRIMARY KEY,
    context_name TEXT NOT NULL,
    context_type TEXT NOT NULL,
    assumption_load REAL,
    structural_clarity REAL,
    constraint_discrimination REAL,
    reconstruction_quality REAL,
    adaptive_potential REAL,
    evidence_contact REAL,
    ethical_visibility REAL,
    implementation_feasibility REAL
);
CREATE VIEW first_principles_profile_scores AS
SELECT context_id, context_name, context_type,
ROUND(-0.16*assumption_load + 0.18*structural_clarity + 0.18*constraint_discrimination + 0.18*reconstruction_quality + 0.14*adaptive_potential + 0.10*evidence_contact + 0.10*ethical_visibility + 0.08*implementation_feasibility, 4) AS profile_score
FROM strategy_contexts;
