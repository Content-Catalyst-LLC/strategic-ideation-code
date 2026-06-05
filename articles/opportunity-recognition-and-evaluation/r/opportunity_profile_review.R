# Advanced R workflow for opportunity profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/opportunity_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

opps <- read.csv(file.path(raw_dir, "opportunities.csv"))

opps$profile_score <-
  0.13 * opps$signal_strength +
  0.14 * opps$capability_alignment +
  0.12 * opps$desirability +
  0.12 * opps$viability +
  0.10 * opps$timing +
  0.12 * opps$learning_value +
  0.11 * opps$option_value +
  0.10 * opps$strategic_fit +
  0.10 * opps$ethical_resilience -
  0.14 * opps$risk

opps$confidence_adjusted_score <- opps$profile_score * opps$evidence_confidence
opps$risk_adjusted_learning <- opps$learning_value + opps$option_value - opps$risk

write.csv(
  opps[order(-opps$profile_score), ],
  file.path(out_tables, "r_opportunity_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(opps, aes(x = reorder(opportunity_name, profile_score), y = profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Opportunity Profile Scores",
      x = "Opportunity",
      y = "Profile Score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_opportunity_profile_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(opps, aes(x = risk, y = learning_value, size = option_value, label = opportunity_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Risk, Learning Value, and Option Value",
      x = "Risk",
      y = "Learning Value",
      size = "Option Value"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_risk_learning_option_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_opportunity_profile_scores_base.png"), width = 1100, height = 800)
  barplot(
    opps$profile_score,
    names.arg = opps$opportunity_id,
    main = "Opportunity Profile Scores",
    ylab = "Profile Score"
  )
  dev.off()
}

print(opps[, c("opportunity_id", "opportunity_name", "profile_score", "confidence_adjusted_score")])
