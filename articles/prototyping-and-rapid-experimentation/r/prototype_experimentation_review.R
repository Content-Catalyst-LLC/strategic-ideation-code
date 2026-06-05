# Advanced R workflow for prototyping and rapid experimentation review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/prototype_experimentation_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

systems <- read.csv(file.path(raw_dir, "experimentation_systems.csv"))

systems$experimentation_profile_score <-
  0.10 * systems$speed +
  0.09 * systems$cost_efficiency +
  0.15 * systems$insight_depth +
  0.12 * systems$user_validation +
  0.12 * systems$assumption_criticality +
  0.14 * systems$evidence_quality +
  0.10 * systems$systems_awareness +
  0.08 * systems$ethical_review +
  0.10 * systems$decision_linkage +
  0.10 * systems$learning_memory

systems$superficial_testing_risk <-
  0.14 * systems$speed +
  0.16 * (1 - systems$insight_depth) +
  0.15 * (1 - systems$evidence_quality) +
  0.13 * (1 - systems$systems_awareness) +
  0.13 * (1 - systems$ethical_review) +
  0.13 * (1 - systems$decision_linkage) +
  0.09 * (1 - systems$assumption_criticality) +
  0.07 * (1 - systems$learning_memory)

systems$diagnosis <- ifelse(
  systems$experimentation_profile_score >= 0.66,
  "strong_experimentation_learning_system",
  ifelse(
    systems$superficial_testing_risk >= 0.62,
    "high_superficial_testing_or_prototype_theater_risk",
    ifelse(systems$decision_linkage < 0.42, "learning_not_linked_to_decisions", "developing_experimentation_capability")
  )
)

write.csv(
  systems[order(-systems$experimentation_profile_score), ],
  file.path(out_tables, "r_prototype_experimentation_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(systems, aes(x = reorder(system_name, experimentation_profile_score), y = experimentation_profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Experimentation Learning Profile",
      x = "System",
      y = "Profile score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_experimentation_profile_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(systems, aes(x = reorder(system_name, superficial_testing_risk), y = superficial_testing_risk)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Superficial Testing Risk",
      x = "System",
      y = "Risk"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_superficial_testing_risk.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_experimentation_profile_scores_base.png"), width = 1100, height = 800)
  barplot(
    systems$experimentation_profile_score,
    names.arg = systems$system_id,
    main = "Experimentation Profile Scores",
    ylab = "Score"
  )
  dev.off()
}

print(systems[, c("system_id", "system_name", "experimentation_profile_score", "superficial_testing_risk", "diagnosis")])
