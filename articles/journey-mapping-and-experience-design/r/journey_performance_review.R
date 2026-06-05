# Advanced R workflow for journey performance review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/journey_performance_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

journeys <- read.csv(file.path(raw_dir, "journey_contexts.csv"))

journeys$journey_profile_score <-
  0.15 * journeys$clarity +
  0.12 * journeys$emotional_confidence -
  0.18 * journeys$friction +
  0.14 * journeys$transition_quality +
  0.12 * journeys$accessibility +
  0.12 * journeys$trust +
  0.10 * journeys$completion_support +
  0.10 * journeys$backstage_alignment +
  0.07 * journeys$measurement_quality

journeys$redesign_need_score <-
  0.22 * journeys$friction +
  0.16 * (1 - journeys$transition_quality) +
  0.14 * (1 - journeys$accessibility) +
  0.13 * (1 - journeys$trust) +
  0.12 * (1 - journeys$clarity) +
  0.11 * (1 - journeys$backstage_alignment) +
  0.07 * (1 - journeys$completion_support) +
  0.05 * (1 - journeys$measurement_quality)

journeys$diagnosis <- ifelse(
  journeys$journey_profile_score >= 0.58,
  "strong_experience_design_profile",
  ifelse(
    journeys$redesign_need_score >= 0.62,
    "high_redesign_priority",
    ifelse(journeys$transition_quality < 0.45, "transition_and_handoff_failure", "developing_journey_quality")
  )
)

write.csv(
  journeys[order(-journeys$journey_profile_score), ],
  file.path(out_tables, "r_journey_performance_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(journeys, aes(x = reorder(journey_name, journey_profile_score), y = journey_profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Journey Experience Profile Scores",
      x = "Journey",
      y = "Profile score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_journey_profile_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(journeys, aes(x = reorder(journey_name, redesign_need_score), y = redesign_need_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Journey Redesign Need",
      x = "Journey",
      y = "Need"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_redesign_need_scores.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_journey_profile_scores_base.png"), width = 1100, height = 800)
  barplot(
    journeys$journey_profile_score,
    names.arg = journeys$journey_id,
    main = "Journey Profile Scores",
    ylab = "Score"
  )
  dev.off()
}

print(journeys[, c("journey_id", "journey_name", "journey_profile_score", "redesign_need_score", "diagnosis")])
