args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) == 0) script_path <- "r/strategic_option_value_review.R"
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
raw_dir <- file.path(root, "data", "raw")
out_tables <- file.path(root, "outputs", "tables")
out_figures <- file.path(root, "outputs", "figures")
dir.create(out_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(out_figures, recursive = TRUE, showWarnings = FALSE)
options <- read.csv(file.path(raw_dir, "strategic_options.csv"))
options$option_value_score <- 0.10*options$initial_return + 0.17*options$learning_value + 0.17*options$flexibility + 0.12*options$reversibility + 0.11*options$scalability + 0.13*options$modularity - 0.14*options$lock_in_exposure - 0.06*options$carrying_cost + 0.11*options$governance_readiness + 0.09*options$ethical_resilience
options$lock_in_warning <- 0.30*options$lock_in_exposure + 0.18*(1-options$reversibility) + 0.16*(1-options$flexibility) + 0.14*(1-options$modularity) + 0.12*(1-options$governance_readiness) + 0.10*(1-options$ethical_resilience)
write.csv(options[order(-options$option_value_score), ], file.path(out_tables, "r_strategic_option_value_review.csv"), row.names = FALSE)
print(options[, c("option_id", "option_name", "option_value_score", "lock_in_warning")])
