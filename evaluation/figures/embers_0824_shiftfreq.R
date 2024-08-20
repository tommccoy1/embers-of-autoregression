

base_size <- 16
theme_set(theme_bw(base_size=base_size) +
            theme(#panel.grid.major=element_blank(),
              panel.grid.minor=element_blank(),
              axis.text.x=element_text()))


counts_c4 <- c(59,21,117,5,15,12,6,3,1,3,3,7,1225,5,2,4,2,2,1,1,4,2,17,3,7)
positions <- 1:25
text_x <- c(1,2,3,4,5,6,7,8,9,10,11,11.8,13,14.2,15,16,17,18,19,20,21,22,23,24,25)

shift_df <- data.frame(Accuracy=counts_c4,
                       Shift=positions,
                       XPosition=text_x
)


ggplot(data=shift_df, aes(x=Shift, y=Accuracy, label=Accuracy)) + 
  geom_point(size=3) + 
  geom_line() +
  geom_text(hjust=0.5, vjust=-1,x=shift_df$XPosition) +
  #geom_text_repel(aes(label=Accuracy), nudge_y=1) +
  ylim(0.0,1350) +
  #xlim(0.0,1.0) +
  scale_x_continuous(breaks=seq(1,25,1)) +
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank()) +
  labs(x="Shift", y="Occurrences in the C4 dataset")

ggsave(file.path("~", 'embers_0824_shifts_counts.pdf'), width=9, height=4)

ggplot(data=shift_df, aes(x=Shift, y=Accuracy, label=Accuracy)) + 
  geom_point(size=3) + 
  geom_line() +
  geom_text(hjust=0.5, vjust=-1,x=shift_df$XPosition) +
  #geom_text_repel(aes(label=Accuracy), nudge_y=1) +
  ylim(0.0,1350) +
  #xlim(0.0,1.0) +
  scale_x_continuous(breaks=seq(1,25,1)) +
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank()) +
  labs(x="Shift", y="Occurrences in corpus")

ggsave(file.path("~", 'embers_0824_shifts_counts_short.pdf'), width=9, height=3.1)


