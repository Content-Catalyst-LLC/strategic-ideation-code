# Advanced R workflow for layered strategy diagnosis.
# Uses base R only by default. If ggplot2 is installed, it also creates a chart.

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

contexts <- read.csv(file.path(raw_dir, "layer_profile_contexts.csv"))
initiatives <- read.csv(file.path(raw_dir, "strategic_initiatives.csv"))
tactics <- read.csv(file.path(raw_dir, "tactical_actions.csv"))

contexts$layer_alignment_score <-
  0.16 * contexts$ideation_quality +
  0.20 * contexts$strategic_clarity +
  0.18 * contexts$tactical_alignment +
  0.14 * contexts$feedback_quality +
  0.14 * contexts$adaptive_learning +
  0.08 * contexts$decision_memory +
  0.10 * contexts$ethical_legitimacy

contexts$diagnosis <- ifelse(
  contexts$tactical_alignment >= 0.65 & contexts$strategic_clarity < 0.55,
  "tactical_overload",
  ifelse(
    contexts$ideation_quality >= 0.75 & contexts$strategic_clarity < 0.55,
    "selection_gap",
    ifelse(
      contexts$strategic_clarity >= 0.70 & contexts$tactical_alignment < 0.55,
      "translation_gap",
      ifelse(contexts$feedback_quality < 0.55, "learning_gap", "monitor")
    )
  )
)

initiatives$portfolio_score <-
  0.22 * initiatives$strategic_fit +
  0.14 * initiatives$implementation_feasibility +
  0.18 * initiatives$systems_leverage +
  0.14 * initiatives$learning_value +
  0.18 * initiatives$ethical_legitimacy -
  0.08 * initiatives$uncertainty

tactics$translation_score <-
  0.26 * tactics$alignment_to_strategy +
  0.20 * tactics$execution_readiness +
  0.16 * tactics$resource_fit +
  0.18 * tactics$feedback_capture +
  0.20 * tactics$learning_routing -
  0.12 * tactics$delivery_risk

write.csv(contexts, file.path(out_tables, "r_layer_context_scores.csv"), row.names = FALSE)
write.csv(initiatives[order(-initiatives$portfolio_score), ], file.path(out_tables, "r_initiative_scores.csv"), row.names = FALSE)
write.csv(tactics[order(tactics$translation_score), ], file.path(out_tables, "r_tactical_translation_scores.csv"), row.names = FALSE)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(contexts, aes(x = reorder(context_name, layer_alignment_score), y = layer_alignment_score)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Layer Alignment by Strategic Context",
      x = "Context",
      y = "Layer alignment score"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_layer_alignment_scores.png"), width = 10, height = 7, dpi = 160)
} else {
  png(file.path(out_figures, "r_layer_alignment_scores_base.png"), width = 1000, height = 700)
  barplot(
    contexts$layer_alignment_score,
    names.arg = contexts$context_id,
    main = "Layer Alignment by Context",
    ylab = "Layer alignment score"
  )
  dev.off()
}

print(contexts[, c("context_id", "context_name", "layer_alignment_score", "diagnosis")])
