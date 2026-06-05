# Advanced R workflow for knowledge architecture profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/knowledge_architecture_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

ideas <- read.csv(file.path(raw_dir, "idea_records.csv"))

ideas$architecture_strength <-
  0.11 * ideas$taxonomy_quality +
  0.12 * ideas$metadata_completeness +
  0.11 * ideas$semantic_clarity +
  0.12 * ideas$evidence_linkage +
  0.11 * ideas$assumption_clarity +
  0.11 * ideas$relationship_mapping +
  0.12 * ideas$retrieval_readiness +
  0.09 * ideas$decision_memory +
  0.07 * ideas$stewardship_quality +
  0.04 * ideas$ethical_representation

ideas$architecture_risk <-
  0.11 * (1 - ideas$taxonomy_quality) +
  0.12 * (1 - ideas$metadata_completeness) +
  0.12 * (1 - ideas$semantic_clarity) +
  0.13 * (1 - ideas$evidence_linkage) +
  0.12 * (1 - ideas$assumption_clarity) +
  0.10 * (1 - ideas$relationship_mapping) +
  0.12 * (1 - ideas$retrieval_readiness) +
  0.09 * (1 - ideas$decision_memory) +
  0.06 * (1 - ideas$stewardship_quality) +
  0.03 * (1 - ideas$ethical_representation)

write.csv(
  ideas[order(-ideas$architecture_strength), ],
  file.path(out_tables, "r_knowledge_architecture_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(ideas, aes(x = reorder(idea_title, architecture_strength), y = architecture_strength)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Idea Architecture Strength",
      x = "Strategic Idea",
      y = "Architecture Strength"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_idea_architecture_strength.png"), width = 11, height = 8, dpi = 160)

  ggplot(ideas, aes(x = architecture_risk, y = architecture_strength, size = retrieval_readiness, label = idea_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Architecture Risk and Retrieval Readiness",
      x = "Architecture Risk",
      y = "Architecture Strength",
      size = "Retrieval Readiness"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_architecture_risk_reuse_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_idea_architecture_strength_base.png"), width = 1100, height = 800)
  barplot(
    ideas$architecture_strength,
    names.arg = ideas$idea_id,
    main = "Strategic Idea Architecture Strength",
    ylab = "Architecture Strength"
  )
  dev.off()
}

print(ideas[, c("idea_id", "idea_title", "architecture_strength", "architecture_risk")])
