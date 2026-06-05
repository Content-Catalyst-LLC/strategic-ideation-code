PRAGMA foreign_keys=ON;
DROP VIEW IF EXISTS base_weighted_scores; DROP VIEW IF EXISTS confidence_adjusted_scores; DROP VIEW IF EXISTS ethical_threshold_review;
DROP TABLE IF EXISTS scores; DROP TABLE IF EXISTS options; DROP TABLE IF EXISTS criteria; DROP TABLE IF EXISTS weight_sets;
CREATE TABLE options(option_id TEXT PRIMARY KEY, option_name TEXT, option_type TEXT, description TEXT);
CREATE TABLE criteria(criterion_id TEXT PRIMARY KEY, criterion_name TEXT, criterion_type TEXT, description TEXT, default_weight REAL, ethical_threshold REAL, non_compensatory TEXT);
CREATE TABLE scores(option_id TEXT PRIMARY KEY, strategic_fit REAL, impact REAL, feasibility REAL, risk_control REAL, learning_value REAL, option_value REAL, ethical_resilience REAL, evidence_confidence REAL, score_notes TEXT);
CREATE TABLE weight_sets(weight_set TEXT PRIMARY KEY, strategic_fit REAL, impact REAL, feasibility REAL, risk_control REAL, learning_value REAL, option_value REAL, ethical_resilience REAL, evidence_confidence REAL, description TEXT);
CREATE VIEW base_weighted_scores AS
SELECT o.option_id,o.option_name,ROUND(w.strategic_fit*s.strategic_fit+w.impact*s.impact+w.feasibility*s.feasibility+w.risk_control*s.risk_control+w.learning_value*s.learning_value+w.option_value*s.option_value+w.ethical_resilience*s.ethical_resilience+w.evidence_confidence*s.evidence_confidence,4) AS base_score
FROM options o JOIN scores s ON o.option_id=s.option_id JOIN weight_sets w ON w.weight_set='base';
CREATE VIEW confidence_adjusted_scores AS
SELECT b.option_id,b.option_name,b.base_score,s.evidence_confidence,ROUND(b.base_score*s.evidence_confidence,4) AS confidence_adjusted_score FROM base_weighted_scores b JOIN scores s ON b.option_id=s.option_id;
CREATE VIEW ethical_threshold_review AS
SELECT option_id,CASE WHEN risk_control<0.35 OR ethical_resilience<0.50 THEN 'threshold_review_required' ELSE 'passes_defined_thresholds' END AS threshold_status,risk_control,ethical_resilience FROM scores;
