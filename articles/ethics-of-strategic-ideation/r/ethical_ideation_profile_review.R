# Advanced R workflow for ethics of strategic ideation profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/ethical_ideation_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

ideas <- read.csv(file.path(raw_dir, "ethical_ideas.csv"))

ideas$ethical_legitimacy <-
  0.12 * ideas$stakeholder_voice +
  0.12 * ideas$evidence_integrity +
  0.10 * ideas$burden_visibility +
  0.09 * ideas$uncertainty_visibility +
  0.08 * ideas$reversibility +
  0.11 * ideas$long_term_responsibility +
  0.07 * ideas$ai_governance +
  0.09 * ideas$accountability +
  0.07 * ideas$redress_quality +
  0.08 * ideas$problem_frame_integrity +
  0.07 * ideas$power_review

ideas$ethical_risk <-
  0.13 * (1 - ideas$stakeholder_voice) +
  0.12 * (1 - ideas$evidence_integrity) +
  0.12 * (1 - ideas$burden_visibility) +
  0.10 * (1 - ideas$uncertainty_visibility) +
  0.09 * (1 - ideas$reversibility) +
  0.10 * (1 - ideas$long_term_responsibility) +
  0.10 * (1 - ideas$ai_governance) +
  0.08 * (1 - ideas$accountability) +
  0.07 * (1 - ideas$redress_quality) +
  0.05 * (1 - ideas$problem_frame_integrity) +
  0.04 * (1 - ideas$power_review)

write.csv(
  ideas[order(-ideas$ethical_legitimacy), ],
  file.path(out_tables, "r_ethical_ideation_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(ideas, aes(x = reorder(idea, ethical_legitimacy), y = ethical_legitimacy)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Ethical Legitimacy of Strategic Ideas",
      x = "Idea",
      y = "Ethical Legitimacy"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_ethical_legitimacy.png"), width = 11, height = 8, dpi = 160)

  ggplot(ideas, aes(x = ethical_risk, y = ethical_legitimacy, size = burden_visibility, label = idea_id)) +
    geom_point(alpha = 0.75) +
    geom_text(nudge_y = 0.03, check_overlap = TRUE) +
    labs(
      title = "Ethical Risk and Legitimacy",
      x = "Ethical Risk",
      y = "Ethical Legitimacy",
      size = "Burden Visibility"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_ethical_risk_legitimacy_map.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_ethical_legitimacy_base.png"), width = 1100, height = 800)
  barplot(
    ideas$ethical_legitimacy,
    names.arg = ideas$idea_id,
    main = "Ethical Legitimacy of Strategic Ideas",
    ylab = "Ethical Legitimacy"
  )
  dev.off()
}

print(ideas[, c("idea_id", "idea", "ethical_legitimacy", "ethical_risk")])
