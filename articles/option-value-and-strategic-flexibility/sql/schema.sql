PRAGMA foreign_keys = ON;
DROP VIEW IF EXISTS option_value_scores;
DROP TABLE IF EXISTS strategic_options;
CREATE TABLE strategic_options (
  option_id TEXT PRIMARY KEY,
  option_name TEXT NOT NULL,
  option_type TEXT NOT NULL,
  initial_return REAL,
  learning_value REAL,
  flexibility REAL,
  reversibility REAL,
  scalability REAL,
  modularity REAL,
  lock_in_exposure REAL,
  carrying_cost REAL,
  governance_readiness REAL,
  ethical_resilience REAL,
  description TEXT
);
CREATE VIEW option_value_scores AS
SELECT option_id, option_name, option_type,
ROUND(0.10*initial_return + 0.17*learning_value + 0.17*flexibility + 0.12*reversibility + 0.11*scalability + 0.13*modularity - 0.14*lock_in_exposure - 0.06*carrying_cost + 0.11*governance_readiness + 0.09*ethical_resilience, 4) AS option_value_score,
ROUND(0.30*lock_in_exposure + 0.18*(1-reversibility) + 0.16*(1-flexibility) + 0.14*(1-modularity) + 0.12*(1-governance_readiness) + 0.10*(1-ethical_resilience), 4) AS lock_in_warning
FROM strategic_options;
