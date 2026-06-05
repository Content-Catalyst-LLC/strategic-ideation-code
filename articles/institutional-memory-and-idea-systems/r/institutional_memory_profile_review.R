# Advanced R workflow for institutional memory and idea systems profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/institutional_memory_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

systems <- read.csv(file.path(raw_dir, "memory_systems.csv"))

systems$memory_strength <-
  0.09 * systems$capture_quality +
  0.11 * systems$metadata_completeness +
  0.11 * systems$context_preservation +
  0.13 * systems$decision_memory +
  0.12 * systems$learning_integration +
  0.12 * systems$retrieval_readiness +
  0.10 * systems$reuse_potential +
  0.08 * systems$stewardship_quality +
  0.06 * systems$continuity_resilience +
  0.05 * systems$ethical_memory +
  0.03 * systems$ai_governance

systems$memory_failure_risk <-
  0.09 * (1 - systems$capture_quality) +
  0.11 * (1 - systems$metadata_completeness) +
  0.11 * (1 - systems$context_preservation) +
  0.13 * (1 - systems$decision_memory) +
  0.12 * (1 - systems$learning_integration) +
  0.12 * (1 - systems$retrieval_readiness) +
  0.09 * (1 - systems$reuse_potential) +
  0.08 * (1 - systems$stewardship_quality) +
  0.07 * (1 - systems$continuity_resilience) +
  0.05 * (1 - systems$ethical_memory) +
  0.03 * (1 - systems$ai_governance)

write.csv(
  systems[order(-systems$memory_strength), ],
  file.path(out_tables, "r_institutional_memory_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(systems, aes(x = reorder(system_area, memory_strength), y = memory_strength)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Institutional Idea Memory Strength",
      x = "System Area",
      y = "Memory Strength"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_institutional_memory_strength.png"), width = 11, height = 8, dpi = 160)

  ggplot(systems, aes(x = memory_failure_risk, y = memory_strength, size = reuse_potential, label = system_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Memory Failure Risk and Reuse Potential",
      x = "Memory Failure Risk",
      y = "Memory Strength",
      size = "Reuse Potential"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_memory_risk_reuse_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_institutional_memory_strength_base.png"), width = 1100, height = 800)
  barplot(
    systems$memory_strength,
    names.arg = systems$system_id,
    main = "Institutional Idea Memory Strength",
    ylab = "Memory Strength"
  )
  dev.off()
}

print(systems[, c("system_id", "system_area", "memory_strength", "memory_failure_risk")])
