# Advanced R workflow for design thinking capability review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/design_capability_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

contexts <- read.csv(file.path(raw_dir, "design_contexts.csv"))

contexts$design_capability_score <-
  0.12 * contexts$empathy_depth +
  0.13 * contexts$reframing_capacity +
  0.10 * contexts$divergence_quality +
  0.10 * contexts$convergence_quality +
  0.12 * contexts$prototyping_strength +
  0.12 * contexts$testing_quality +
  0.11 * contexts$systems_awareness +
  0.10 * contexts$ethical_review +
  0.10 * contexts$decision_linkage +
  0.06 * contexts$adaptability +
  0.04 * contexts$institutional_memory

contexts$superficiality_risk <-
  0.18 * (1 - contexts$empathy_depth) +
  0.14 * (1 - contexts$reframing_capacity) +
  0.12 * (1 - contexts$testing_quality) +
  0.12 * (1 - contexts$systems_awareness) +
  0.12 * (1 - contexts$ethical_review) +
  0.16 * (1 - contexts$decision_linkage) +
  0.10 * (1 - contexts$institutional_memory) +
  0.06 * (1 - contexts$adaptability)

contexts$diagnosis <- ifelse(
  contexts$design_capability_score >= 0.72,
  "strong_design_thinking_capability",
  ifelse(
    contexts$superficiality_risk >= 0.62,
    "high_superficiality_risk",
    ifelse(contexts$decision_linkage < 0.45, "weak_decision_linkage", "developing_capability")
  )
)

write.csv(
  contexts[order(-contexts$design_capability_score), ],
  file.path(out_tables, "r_design_capability_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(contexts, aes(x = reorder(context_name, design_capability_score), y = design_capability_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Design Thinking Capability Scores",
      x = "Context",
      y = "Capability"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_design_capability_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(contexts, aes(x = reorder(context_name, superficiality_risk), y = superficiality_risk)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Risk of Superficial Design Thinking",
      x = "Context",
      y = "Risk"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_superficiality_risk.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_design_capability_scores_base.png"), width = 1100, height = 800)
  barplot(
    contexts$design_capability_score,
    names.arg = contexts$context_id,
    main = "Design Thinking Capability Scores",
    ylab = "Capability"
  )
  dev.off()
}

print(contexts[, c("context_id", "context_name", "design_capability_score", "superficiality_risk", "diagnosis")])
