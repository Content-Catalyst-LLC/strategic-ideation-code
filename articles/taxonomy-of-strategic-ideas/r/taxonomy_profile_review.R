# Advanced R workflow for strategic idea taxonomy profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/taxonomy_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

records <- read.csv(file.path(raw_dir, "taxonomy_records.csv"))

records$taxonomy_strength <-
  0.12 * records$category_clarity +
  0.10 * records$level_fit +
  0.10 * records$maturity_accuracy +
  0.12 * records$evidence_classification +
  0.12 * records$function_clarity +
  0.10 * records$relationship_mapping +
  0.12 * records$retrieval_value +
  0.09 * records$governance_strength +
  0.08 * records$ethical_visibility +
  0.05 * records$ai_classification_quality

records$taxonomy_risk <-
  0.12 * (1 - records$category_clarity) +
  0.10 * (1 - records$level_fit) +
  0.10 * (1 - records$maturity_accuracy) +
  0.12 * (1 - records$evidence_classification) +
  0.12 * (1 - records$function_clarity) +
  0.10 * (1 - records$relationship_mapping) +
  0.12 * (1 - records$retrieval_value) +
  0.09 * (1 - records$governance_strength) +
  0.08 * (1 - records$ethical_visibility) +
  0.05 * (1 - records$ai_classification_quality)

write.csv(
  records[order(-records$taxonomy_strength), ],
  file.path(out_tables, "r_taxonomy_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(records, aes(x = reorder(idea_record, taxonomy_strength), y = taxonomy_strength)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Idea Taxonomy Strength",
      x = "Idea Record",
      y = "Taxonomy Strength"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_taxonomy_strength.png"), width = 11, height = 8, dpi = 160)

  ggplot(records, aes(x = taxonomy_risk, y = taxonomy_strength, size = retrieval_value, label = record_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Taxonomy Risk and Retrieval Value",
      x = "Taxonomy Risk",
      y = "Taxonomy Strength",
      size = "Retrieval Value"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_taxonomy_risk_retrieval_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_taxonomy_strength_base.png"), width = 1100, height = 800)
  barplot(
    records$taxonomy_strength,
    names.arg = records$record_id,
    main = "Strategic Idea Taxonomy Strength",
    ylab = "Taxonomy Strength"
  )
  dev.off()
}

print(records[, c("record_id", "idea_record", "taxonomy_strength", "taxonomy_risk")])
