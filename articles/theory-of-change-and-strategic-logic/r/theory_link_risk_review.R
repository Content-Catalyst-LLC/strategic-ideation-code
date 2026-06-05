# Advanced R workflow for theory-of-change link risk.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/theory_link_risk_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

links <- read.csv(file.path(raw_dir, "theory_links.csv"))

links$link_risk_score <-
  0.16 * (1 - links$mechanism_clarity) +
  0.18 * (1 - links$evidence_strength) +
  0.13 * links$actor_dependency +
  0.11 * links$capacity_dependency +
  0.14 * links$system_dependency +
  0.12 * links$ethical_dependency +
  0.16 * links$failure_consequence

links$test_priority_score <- links$link_risk_score * links$testability

links$diagnosis <- ifelse(
  links$link_risk_score >= 0.62 & links$testability >= 0.62,
  "test_first",
  ifelse(
    links$link_risk_score >= 0.62,
    "reduce_commitment_before_scaling",
    ifelse(
      links$evidence_strength <= 0.42,
      "evidence_gap",
      "monitor"
    )
  )
)

write.csv(
  links[order(-links$link_risk_score), ],
  file.path(out_tables, "r_theory_link_risk_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(links, aes(x = reorder(link_id, link_risk_score), y = link_risk_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Theory-of-Change Link Risk",
      x = "Link",
      y = "Risk"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_theory_link_risk_scores.png"), width = 11, height = 8, dpi = 160)

  ggplot(links, aes(x = evidence_strength, y = mechanism_clarity, label = link_id)) +
    geom_point(size = 3) +
    geom_text(nudge_y = 0.02, check_overlap = TRUE) +
    labs(
      title = "Mechanism Clarity and Evidence Strength",
      x = "Evidence Strength",
      y = "Mechanism Clarity"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_mechanism_clarity_evidence.png"), width = 10, height = 7, dpi = 160)
} else {
  png(file.path(out_figures, "r_theory_link_risk_scores_base.png"), width = 1100, height = 800)
  barplot(
    links$link_risk_score,
    names.arg = links$link_id,
    main = "Theory-of-Change Link Risk",
    ylab = "Risk"
  )
  dev.off()
}

print(links[, c("link_id", "idea_id", "link_stage", "link_risk_score", "test_priority_score", "diagnosis")])
