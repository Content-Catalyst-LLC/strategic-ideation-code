# Advanced R workflow for creative constraint diagnostics.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

contexts <- read.csv(file.path(raw_dir, "constraint_contexts.csv"))
options <- read.csv(file.path(raw_dir, "innovation_options.csv"))

contexts$rigidity_pressure <-
  0.24 * contexts$resource_pressure +
  0.25 * contexts$technical_rigidity +
  0.27 * contexts$institutional_rigidity +
  0.24 * contexts$ecological_boundary_pressure

contexts$productivity_profile <-
  -0.10 * contexts$resource_pressure -
  -0.00 * 0 +
  -0.10 * contexts$technical_rigidity -
  0.10 * contexts$institutional_rigidity +
  0.12 * contexts$ecological_boundary_pressure +
  0.16 * contexts$ethical_constraint_visibility +
  0.16 * contexts$search_focus +
  0.16 * contexts$adaptive_opportunity +
  0.14 * contexts$stakeholder_legitimacy +
  0.14 * contexts$learning_capacity +
  0.12 * contexts$implementation_readiness

contexts$rigidity_risk <- contexts$rigidity_pressure * (1 - contexts$learning_capacity)
contexts$diffusion_risk <- (1 - contexts$search_focus) * contexts$adaptive_opportunity
contexts$legitimacy_gap <- pmax(0, 0.65 - contexts$stakeholder_legitimacy)

contexts$diagnosis <- ifelse(
  contexts$diffusion_risk >= 0.42,
  "under_constrained_diffusion_risk",
  ifelse(
    contexts$rigidity_risk >= 0.42,
    "over_constrained_rigidity_risk",
    ifelse(
      contexts$legitimacy_gap >= 0.25,
      "stakeholder_legitimacy_gap",
      ifelse(contexts$productivity_profile >= 0.42, "productive_constraint_profile", "requires_constraint_review")
    )
  )
)

options$innovation_option_score <-
  0.12 * options$novelty +
  0.16 * options$strategic_fit +
  0.14 * options$constraint_fit +
  0.14 * options$adaptive_value +
  0.12 * options$stakeholder_value +
  0.12 * options$ecological_responsibility +
  0.12 * options$ethical_legitimacy +
  0.10 * options$implementation_readiness -
  0.08 * options$assumption_burden

write.csv(contexts[order(-contexts$productivity_profile), ], file.path(out_tables, "r_creative_constraint_profiles.csv"), row.names = FALSE)
write.csv(options[order(-options$innovation_option_score), ], file.path(out_tables, "r_innovation_option_scores.csv"), row.names = FALSE)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(contexts, aes(x = reorder(context_name, productivity_profile), y = productivity_profile)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Productive Constraint Profile Scores",
      x = "Context",
      y = "Profile score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_creative_constraint_profiles.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_creative_constraint_profiles_base.png"), width = 1100, height = 800)
  barplot(
    contexts$productivity_profile,
    names.arg = contexts$context_id,
    main = "Creative Constraint Profile Scores",
    ylab = "Profile score"
  )
  dev.off()
}

print(contexts[, c("context_id", "context_name", "productivity_profile", "rigidity_risk", "diffusion_risk", "diagnosis")])
