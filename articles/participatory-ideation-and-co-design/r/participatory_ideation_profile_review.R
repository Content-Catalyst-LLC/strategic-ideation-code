# Advanced R workflow for participatory ideation and co-design profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/participatory_ideation_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

systems <- read.csv(file.path(raw_dir, "participation_systems.csv"))

systems$participation_quality_score <-
  0.13 * systems$representation +
  0.15 * systems$influence +
  0.11 * systems$accessibility +
  0.11 * systems$reciprocity +
  0.13 * systems$power_awareness +
  0.12 * systems$knowledge_integration +
  0.11 * systems$decision_linkage +
  0.10 * systems$accountability +
  0.04 * systems$learning_memory

systems$tokenism_extraction_risk <-
  0.16 * (1 - systems$influence) +
  0.14 * (1 - systems$decision_linkage) +
  0.14 * (1 - systems$accountability) +
  0.13 * (1 - systems$reciprocity) +
  0.13 * (1 - systems$power_awareness) +
  0.11 * (1 - systems$representation) +
  0.10 * (1 - systems$accessibility) +
  0.09 * (1 - systems$learning_memory)

systems$diagnosis <- ifelse(
  systems$participation_quality_score >= 0.72,
  "strong_participatory_codesign_system",
  ifelse(
    systems$tokenism_extraction_risk >= 0.68,
    "high_tokenism_or_extractive_participation_risk",
    ifelse(systems$influence < 0.36, "participation_has_low_decision_influence", "developing_participatory_capability")
  )
)

write.csv(
  systems[order(-systems$participation_quality_score), ],
  file.path(out_tables, "r_participatory_ideation_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(systems, aes(x = reorder(system_name, participation_quality_score), y = participation_quality_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Participatory Ideation Quality",
      x = "System",
      y = "Quality score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_participation_quality_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(systems, aes(x = reorder(system_name, tokenism_extraction_risk), y = tokenism_extraction_risk)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Tokenism and Extraction Risk",
      x = "System",
      y = "Risk"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_tokenism_extraction_risk.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_participation_quality_scores_base.png"), width = 1100, height = 800)
  barplot(
    systems$participation_quality_score,
    names.arg = systems$system_id,
    main = "Participation Quality Scores",
    ylab = "Score"
  )
  dev.off()
}

print(systems[, c("system_id", "system_name", "participation_quality_score", "tokenism_extraction_risk", "diagnosis")])
