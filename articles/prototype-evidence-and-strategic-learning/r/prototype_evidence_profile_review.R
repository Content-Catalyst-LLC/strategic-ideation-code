# Advanced R workflow for prototype evidence and strategic learning profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/prototype_evidence_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

systems <- read.csv(file.path(raw_dir, "prototype_systems.csv"))

systems$prototype_learning_quality <-
  0.13 * systems$assumption_clarity +
  0.13 * systems$learning_target_fit +
  0.15 * systems$evidence_quality +
  0.13 * systems$behavioral_grounding +
  0.11 * systems$context_realism +
  0.11 * systems$systems_awareness +
  0.11 * systems$decision_linkage +
  0.07 * systems$ethical_review +
  0.06 * systems$learning_memory

systems$validation_theater_risk <-
  0.17 * (1 - systems$assumption_clarity) +
  0.16 * (1 - systems$evidence_quality) +
  0.14 * (1 - systems$behavioral_grounding) +
  0.13 * (1 - systems$decision_linkage) +
  0.12 * (1 - systems$learning_memory) +
  0.11 * (1 - systems$systems_awareness) +
  0.09 * (1 - systems$ethical_review) +
  0.08 * (1 - systems$context_realism)

systems$diagnosis <- ifelse(
  systems$prototype_learning_quality >= 0.72,
  "strong_prototype_learning_system",
  ifelse(
    systems$validation_theater_risk >= 0.68,
    "high_validation_theater_risk",
    ifelse(systems$behavioral_grounding < 0.36, "evidence_lacks_behavioral_grounding", "developing_prototype_learning_capability")
  )
)

write.csv(
  systems[order(-systems$prototype_learning_quality), ],
  file.path(out_tables, "r_prototype_evidence_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(systems, aes(x = reorder(system_name, prototype_learning_quality), y = prototype_learning_quality)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Prototype Learning Quality",
      x = "System",
      y = "Quality score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_prototype_learning_quality.png"), width = 11, height = 8, dpi = 160)

  ggplot(systems, aes(x = reorder(system_name, validation_theater_risk), y = validation_theater_risk)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Validation Theater Risk",
      x = "System",
      y = "Risk"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_validation_theater_risk.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_prototype_learning_quality_base.png"), width = 1100, height = 800)
  barplot(
    systems$prototype_learning_quality,
    names.arg = systems$system_id,
    main = "Prototype Learning Quality",
    ylab = "Score"
  )
  dev.off()
}

print(systems[, c("system_id", "system_name", "prototype_learning_quality", "validation_theater_risk", "diagnosis")])
