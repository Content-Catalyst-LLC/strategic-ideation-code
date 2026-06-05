# Advanced R workflow for game theory and strategic interaction profile review.
# Uses base R only by default. If ggplot2 is installed, it also creates charts.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) {
  script_path <- "r/strategic_interaction_profile_review.R"
}

root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")

dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)

profiles <- read.csv(file.path(raw_dir, "strategic_interaction_profiles.csv"))

profiles$strategic_interaction_score <-
  0.12 * profiles$rivalry +
  0.18 * profiles$coordination_potential +
  0.12 * profiles$information_asymmetry +
  0.10 * profiles$retaliation_risk +
  0.15 * profiles$institutional_support +
  0.12 * profiles$behavioral_realism +
  0.15 * profiles$mechanism_design_potential +
  0.06 * profiles$ethical_complexity

profiles$cooperation_fragility <-
  0.22 * profiles$rivalry +
  0.20 * profiles$retaliation_risk +
  0.16 * profiles$information_asymmetry +
  0.12 * profiles$ethical_complexity -
  0.15 * profiles$institutional_support -
  0.15 * profiles$coordination_potential

profiles$mechanism_opportunity <-
  0.30 * profiles$mechanism_design_potential +
  0.18 * profiles$coordination_potential +
  0.16 * profiles$information_asymmetry +
  0.14 * profiles$ethical_complexity +
  0.12 * profiles$institutional_support +
  0.10 * profiles$behavioral_realism

write.csv(
  profiles[order(-profiles$mechanism_opportunity), ],
  file.path(out_tables, "r_strategic_interaction_profile_review.csv"),
  row.names = FALSE
)

if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  ggplot(profiles, aes(x = reorder(setting_name, mechanism_opportunity), y = mechanism_opportunity)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Mechanism-Design Opportunity",
      x = "Setting",
      y = "Opportunity"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_mechanism_design_opportunity.png"), width = 11, height = 8, dpi = 160)

  ggplot(profiles, aes(x = reorder(setting_name, cooperation_fragility), y = cooperation_fragility)) +
    geom_col() +
    coord_flip() +
    labs(
      title = "Cooperation Fragility",
      x = "Setting",
      y = "Fragility"
    ) +
    theme_minimal(base_size = 12)

  ggsave(file.path(out_figures, "r_cooperation_fragility.png"), width = 11, height = 8, dpi = 160)
} else {
  png(file.path(out_figures, "r_mechanism_design_opportunity_base.png"), width = 1100, height = 800)
  barplot(
    profiles$mechanism_opportunity,
    names.arg = profiles$setting_id,
    main = "Mechanism-Design Opportunity",
    ylab = "Opportunity"
  )
  dev.off()
}

print(profiles[, c("setting_id", "setting_name", "strategic_interaction_score", "cooperation_fragility", "mechanism_opportunity")])
