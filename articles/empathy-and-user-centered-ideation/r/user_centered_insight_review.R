# Advanced R workflow for user-centered insight profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/user_centered_insight_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

contexts <- read.csv(file.path(raw_dir, "empathy_contexts.csv"))

contexts$empathy_profile_score <-
  0.16 * contexts$observational_depth -
  0.14 * contexts$projection_risk +
  0.16 * contexts$unmet_need_visibility +
  0.12 * contexts$stakeholder_breadth +
  0.16 * contexts$reframing_potential +
  0.10 * contexts$ethical_review +
  0.10 * contexts$systems_awareness +
  0.14 * contexts$decision_linkage +
  0.10 * contexts$institutional_memory

contexts$superficiality_risk <-
  0.20 * contexts$projection_risk +
  0.16 * (1 - contexts$decision_linkage) +
  0.14 * (1 - contexts$observational_depth) +
  0.12 * (1 - contexts$unmet_need_visibility) +
  0.12 * (1 - contexts$ethical_review) +
  0.10 * (1 - contexts$systems_awareness) +
  0.08 * (1 - contexts$stakeholder_breadth) +
  0.08 * (1 - contexts$institutional_memory)

contexts$diagnosis <- ifelse(
  contexts$empathy_profile_score >= 0.64,
  "strong_user_centered_ideation_capability",
  ifelse(
    contexts$superficiality_risk >= 0.62,
    "high_empathy_theater_or_projection_risk",
    ifelse(contexts$decision_linkage < 0.42, "insight_not_linked_to_decisions", "developing_capability")
  )
)

write.csv(
  contexts[order(-contexts$empathy_profile_score), ],
  file.path(out_tables, "r_user_centered_insight_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(contexts, aes(x = reorder(context_name, empathy_profile_score), y = empathy_profile_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Empathy and User-Centered Ideation Profile",
      x = "Context",
      y = "Profile score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_empathy_profile_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(contexts, aes(x = reorder(context_name, superficiality_risk), y = superficiality_risk)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Risk of Superficial Empathy",
      x = "Context",
      y = "Risk"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_superficial_empathy_risk.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_empathy_profile_scores_base.png"), width = 1100, height = 800)
  barplot(
    contexts$empathy_profile_score,
    names.arg = contexts$context_id,
    main = "Empathy Profile Scores",
    ylab = "Score"
  )
  dev.off()
}

print(contexts[, c("context_id", "context_name", "empathy_profile_score", "superficiality_risk", "diagnosis")])
