

library(ggplot2)



base_size <- 20
theme_set(theme_bw(base_size=base_size) +
            theme(#panel.grid.major=element_blank(),
              panel.grid.minor=element_blank(),
              axis.text.x=element_text()))






# ENCRYPTING
logprob_rev <- c(-144.53, -86.25, -58.38)
logprob_pig <- c(-132.26, -86.86, -62.54)
logprob_rot <- c(-144.54, -86.25, -58.38)
logprob_acronym <- c(-147.11,-134.49,-122.29,-109.05,-93.54)
logprob_birthday <- c(-15.01, -13.31, -11.23, -9.09)
logprob_countchar <- c(-19.78, -3.87)
logprob_countword <- c(-16.97, -10.94)




accs_gpt35_rev <- c(0.37,0.33,0.46)
accs_gpt35_pig <- c(0.25,0.22,0.30)
accs_gpt35_rot <- c(0.05,0.03,0.02)
accs_gpt35_acronym <- c(0.292,0.305,0.32,0.329,0.391)
accs_gpt35_birthday <- c(0.09, 0.38, 0.86, 0.99)
accs_gpt35_countchar <- c(0.219,0.338)
accs_gpt35_countword <- c(0.143,0.127)


accs_gpt4_rev <- c(0.81,0.76,0.87)
accs_gpt4_pig <- c(0.39,0.38,0.39)
accs_gpt4_rot <- c(0.11,0.10,0.21)
accs_gpt4_acronym <- c(0.731,0.746,0.728,0.756,0.762)
accs_gpt4_birthday <- c(0.23, 0.56, 0.91, 0.99)
accs_gpt4_countchar <- c(0.240,0.271)
accs_gpt4_countword <- c(0.220,0.234)


accs_llama3_rev <- c(0.03, 0.02, 0.05)
accs_llama3_pig <- c(0.03, 0.03, 0.05)
accs_llama3_rot <- c(0.00, 0.00, 0.00)
accs_llama3_acronym <- c(0.481, 0.495, 0.568, 0.57, 0.544)
accs_llama3_birthday <- c(0.17, 0.54, 0.85, 0.95)
accs_llama3_countchar <- c(0.162, 0.172)
accs_llama3_countword <- c(0.086, 0.087)


accs_claude3_rev <- c(0.24, 0.90, 0.95)
accs_claude3_pig <- c(0.55, 0.57, 0.66)
accs_claude3_rot <- c(0.54,0.62, 0.70)
accs_claude3_acronym <- c(0.521, 0.479, 0.475,0.442,0.577)
accs_claude3_birthday <- c(0.16, 0.54, 0.88, 0.98)
accs_claude3_countchar <- c(0.508, 0.357)
accs_claude3_countword <- c(0.250, 0.262)

accs_geminipro_rev <- c(0.06, 0.25, 0.30)
accs_geminipro_pig <- c(0.00, 0.00, 0.00)
accs_geminipro_rot <- c(0.00, 0.00, 0.00)
accs_geminipro_acronym <- c(0.478, 0.488, 0.505, 0.531, 0.547)
accs_geminipro_birthday <- c(0.05, 0.21, 0.63, 0.97)
accs_geminipro_countchar <- c(0.154, 0.222)
accs_geminipro_countword <- c(0.132, 0.144)

accs_olmo_rev <- c(0.00, 0.00, 0.00)
accs_olmo_pig <- c(0.00, 0.00, 0.00)
accs_olmo_rot <- c(0.00, 0.00, 0.00)
accs_olmo_acronym <- c(0.000, 0.001, 0.002, 0.006, 0.003)
accs_olmo_birthday <- c(0.00, 0.00, 0.00, 0.04)
accs_olmo_countchar <- c(0.041,0.037)
accs_olmo_countword <- c(0.012, 0.017)


encoding_df <- data.frame(Logprob=rep(c(logprob_rev,logprob_pig,logprob_rot,logprob_acronym,logprob_birthday,logprob_countchar,logprob_countword), 6),
                          StandardError=c(my_se(c(accs_gpt4_rev, accs_gpt4_pig, accs_gpt4_rot), 100), my_se(accs_gpt4_acronym, 1000), my_se(accs_gpt4_birthday, 100), my_se(c(accs_gpt4_countchar, accs_gpt4_countword),  1200),
                                          my_se(c(accs_gpt35_rev, accs_gpt35_pig, accs_gpt35_rot), 100), my_se(accs_gpt35_acronym, 1000), my_se(accs_gpt35_birthday, 100), my_se(c(accs_gpt35_countchar, accs_gpt35_countword),  1200),
                                          my_se(c(accs_claude3_rev, accs_claude3_pig, accs_claude3_rot), 100), my_se(accs_claude3_acronym, 1000), my_se(accs_claude3_birthday, 100), my_se(c(accs_claude3_countchar, accs_claude3_countword),  1200),
                                          my_se(c(accs_llama3_rev, accs_llama3_pig, accs_llama3_rot), 100), my_se(accs_llama3_acronym, 1000), my_se(accs_llama3_birthday, 100), my_se(c(accs_llama3_countchar, accs_llama3_countword),  1200),
                                          my_se(c(accs_geminipro_rev, accs_geminipro_pig, accs_geminipro_rot), 100), my_se(accs_geminipro_acronym, 1000), my_se(accs_geminipro_birthday, 100), my_se(c(accs_geminipro_countchar, accs_geminipro_countword),  1200),
                                          my_se(c(accs_olmo_rev, accs_olmo_pig, accs_olmo_rot), 100), my_se(accs_olmo_acronym, 1000), my_se(accs_olmo_birthday, 100), my_se(c(accs_olmo_countchar, accs_olmo_countword),  1200)), 
                          Accuracy=c(accs_gpt4_rev, accs_gpt4_pig, accs_gpt4_rot, accs_gpt4_acronym, accs_gpt4_birthday, accs_gpt4_countchar, accs_gpt4_countword,
                                     accs_gpt35_rev, accs_gpt35_pig, accs_gpt35_rot, accs_gpt35_acronym, accs_gpt35_birthday, accs_gpt35_countchar, accs_gpt35_countword,
                                     accs_claude3_rev, accs_claude3_pig, accs_claude3_rot, accs_claude3_acronym, accs_claude3_birthday, accs_claude3_countchar, accs_claude3_countword,
                                     accs_llama3_rev, accs_llama3_pig, accs_llama3_rot, accs_llama3_acronym, accs_llama3_birthday, accs_llama3_countchar, accs_llama3_countword,
                                     accs_geminipro_rev, accs_geminipro_pig, accs_geminipro_rot, accs_geminipro_acronym, accs_geminipro_birthday, accs_geminipro_countchar, accs_geminipro_countword,
                                     accs_olmo_rev, accs_olmo_pig, accs_olmo_rot, accs_olmo_acronym, accs_olmo_birthday, accs_olmo_countchar, accs_olmo_countword),
                          Model=rep(c("GPT-4", "GPT-3.5", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"), each=22),
                          Task=rep(c(rep(c("Reversal", "Pig Latin", "Shift cipher"), each=3), rep(c("Acronym"), 5), rep(c("Birthdays"), 4), rep(c("Counting\ncharacters", "Counting\nwords"), each=2)), 6)
)

encoding_df$Task <- factor(encoding_df$Task, levels=c("Shift cipher", "Reversal", "Pig Latin", "Counting\ncharacters", "Counting\nwords", "Acronym", "Birthdays"))
encoding_df$Model <- factor(encoding_df$Model, levels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"))

encoding_df <- encoding_df[encoding_df$Model != "OLMo", ]
encoding_df <- encoding_df[encoding_df$Task != "Counting\ncharacters" & encoding_df$Task != "Counting\nwords", ]
ggplot(data=encoding_df, aes(x=Logprob, y=Accuracy, color=Model, shape=Model)) + 
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  geom_point(size=5) + 
  geom_line(size=1.5) +
  ylim(0.0,1.0) +
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38"), labels=c("GPT-3.5           ", "GPT-4           ", "Claude 3           ", "Llama 3           ", "Gemini 1.0")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38"), labels=c("GPT-3.5           ", "GPT-4           ", "Claude 3           ", "Llama 3           ", "Gemini 1.0")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20), labels=c("GPT-3.5           ", "GPT-4           ", "Claude 3           ", "Llama 3           ", "Gemini 1.0")) +
  facet_grid(. ~ Task, scales="free") +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.key.size = unit(0.8, 'cm')) +
  #theme(legend.position=c(0.92, 0.13)) +
  #theme(legend.position="right") +
  theme(legend.position="top") +
  theme(axis.text.x = element_text(size = 10)) +
  theme(legend.title=element_blank(),
        legend.margin=margin(c(2,2,2,2))) +
  theme(legend.box.spacing = unit(0, "pt"), legend.spacing.x = unit(0, "pt"), legend.spacing.y = unit(0, "pt")) +
  labs(x="Input log probability", y="Accuracy")


ggsave(file.path("~", 'embers_encoding_4may2024.pdf'), width=10.5, height=4.3)











