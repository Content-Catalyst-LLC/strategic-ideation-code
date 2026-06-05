# Advanced R workflow for strategic communication and conceptual coherence profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/communication_coherence_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

profiles <- read.csv(file.path(raw_dir, "communication_profiles.csv"))

profiles$coherence_strength <-
  0.11 * profiles$concept_definition +
  0.11 * profiles$narrative_coherence +
  0.13 * profiles$evidence_integrity +
  0.10 * profiles$audience_adaptation +
  0.13 * profiles$decision_alignment +
  0.11 * profiles$implementation_translatability +
  0.08 * profiles$feedback_quality +
  0.10 * profiles$governance_strength +
  0.09 * profiles$ethical_visibility +
  0.04 * profiles$ai_governance

profiles$meaning_loss_risk <-
  0.12 * (1 - profiles$concept_definition) +
  0.10 * (1 - profiles$narrative_coherence) +
  0.13 * (1 - profiles$evidence_integrity) +
  0.10 * (1 - profiles$audience_adaptation) +
  0.13 * (1 - profiles$decision_alignment) +
  0.11 * (1 - profiles$implementation_translatability) +
  0.08 * (1 - profiles$feedback_quality) +
  0.09 * (1 - profiles$governance_strength) +
  0.10 * (1 - profiles$ethical_visibility) +
  0.04 * (1 - profiles$ai_governance)

write.csv(
  profiles[order(-profiles$coherence_strength), ],
  file.path(out_tables, "r_communication_coherence_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(profiles, aes(x = reorder(communication_profile, coherence_strength), y = coherence_strength)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Strategic Communication Coherence Strength",
      x = "Communication Profile",
      y = "Coherence Strength"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_communication_coherence_strength.png"), width = 11, height = 8, dpi = 160)

  ggplot(profiles, aes(x = meaning_loss_risk, y = coherence_strength, size = ethical_visibility, label = profile_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Meaning Loss Risk and Conceptual Coherence",
      x = "Meaning Loss Risk",
      y = "Coherence Strength",
      size = "Ethical Visibility"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_meaning_loss_coherence_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_communication_coherence_strength_base.png"), width = 1100, height = 800)
  barplot(
    profiles$coherence_strength,
    names.arg = profiles$profile_id,
    main = "Strategic Communication Coherence Strength",
    ylab = "Coherence Strength"
  )
  dev.off()
}

print(profiles[, c("profile_id", "communication_profile", "coherence_strength", "meaning_loss_risk")])
