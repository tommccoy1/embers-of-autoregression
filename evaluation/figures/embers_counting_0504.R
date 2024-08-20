
library(ggplot2)
library(dplyr)
library(ggpattern)


setwd("~/")

base_size <- 16
theme_set(theme_bw(base_size=base_size) +
            theme(#panel.grid.major=element_blank(),
              panel.grid.minor=element_blank(),
              axis.text.x=element_text()))

# GPT-3.5
gpt35_word_common <- c(1.0,1.0,0.9,0.9666666666666667,0.9333333333333333,0.8666666666666667,0.8333333333333334,0.7,0.5,0.6333333333333333,0.5666666666666667,0.6,0.3,0.23333333333333334,0.2,0.0,0.0,0.0,0.0,0.03333333333333333,0.06666666666666667,0.0,0.06666666666666667,0.03333333333333333,0.03333333333333333,0.13333333333333333,0.0,0.0,0.1,0.16666666666666666,0.0,0.0,0.0,0.0,0.0,0.03333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.03333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.13333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.26666666666666666,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.16666666666666666,0.0,0.0,0.0,0.0,0.43333333333333335,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.7)
gpt35_word_rare <- c(1.0,1.0,0.9666666666666667,0.9333333333333333,0.8,0.7666666666666667,0.5333333333333333,0.3,0.16666666666666666,0.43333333333333335,0.26666666666666666,0.3333333333333333,0.06666666666666667,0.03333333333333333,0.03333333333333333,0.03333333333333333,0.0,0.03333333333333333,0.06666666666666667,0.23333333333333334,0.1,0.0,0.2,0.06666666666666667,0.06666666666666667,0.23333333333333334,0.03333333333333333,0.03333333333333333,0.0,0.6333333333333333,0.0,0.1,0.03333333333333333,0.23333333333333334,0.0,0.43333333333333335,0.0,0.06666666666666667,0.0,0.4,0.0,0.03333333333333333,0.06666666666666667,0.0,0.06666666666666667,0.0,0.13333333333333333,0.0,0.0,0.5,0.0,0.0,0.0,0.1,0.0,0.0,0.0,0.0,0.0,0.7333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.4,0.0,0.0,0.0,0.0,0.5333333333333333,0.0,0.0,0.0,0.0,0.13333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.9666666666666667)

gpt35_char_common <- c(1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.6333333333333333,0.9333333333333333,0.4666666666666667,0.5,0.9333333333333333,1.0,0.6333333333333333,0.16666666666666666,0.6,1.0,0.6666666666666666,0.36666666666666664,0.13333333333333333,0.4,0.9666666666666667,0.7,0.5333333333333333,0.13333333333333333,0.4,0.5666666666666667,0.6,0.23333333333333334,0.03333333333333333,0.1,0.7333333333333333,0.7666666666666667,0.7333333333333333,0.3,0.13333333333333333,0.8333333333333334,0.23333333333333334,0.4,0.6333333333333333,0.23333333333333334,0.4,0.43333333333333335,0.3333333333333333,0.3,0.16666666666666666,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.4,0.2,0.16666666666666666,0.3,0.13333333333333333,0.1,0.3333333333333333,0.0,0.0,0.0,0.2,0.0,0.13333333333333333,0.0,0.0,0.36666666666666664,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8)
gpt35_char_rare <- c(1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.9333333333333333,0.7666666666666667,0.8333333333333334,0.7333333333333333,0.5333333333333333,0.43333333333333335,0.7666666666666667,0.7,0.1,0.3333333333333333,0.2,0.16666666666666666,0.03333333333333333,0.06666666666666667,0.0,0.0,0.0,0.13333333333333333,0.0,0.0,0.0,0.0,0.03333333333333333,0.0,0.0,0.0,0.0,0.2,0.0,0.0,0.0,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.3333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3333333333333333,0.0,0.0,0.0,0.0,0.43333333333333335,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0)

# GPT-4
gpt4_word_common <- c(1.0,1.0,1.0,0.9666666666666667,1.0,1.0,1.0,1.0,1.0,1.0,0.8333333333333334,0.9666666666666667,1.0,0.9,0.43333333333333335,0.3,0.9666666666666667,0.8333333333333334,0.26666666666666666,1.0,0.3,0.5,0.5666666666666667,0.36666666666666664,0.1,0.03333333333333333,0.03333333333333333,0.03333333333333333,0.0,0.3333333333333333,0.0,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.3333333333333333,0.0,0.03333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.9666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.43333333333333335,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.7666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0)
gpt4_word_rare <- c(1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.9333333333333333,0.9333333333333333,0.6333333333333333,0.9,0.8,0.5666666666666667,0.43333333333333335,0.3333333333333333,0.8,0.8,0.1,0.9,0.06666666666666667,0.16666666666666666,0.2,0.43333333333333335,0.1,0.0,0.0,0.1,0.0,0.8,0.0,0.0,0.03333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.7333333333333333,0.0,0.03333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.43333333333333335,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.6333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.13333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0)

gpt4_char_common <- c(1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.8333333333333334,0.7666666666666667,0.9333333333333333,1.0,0.5333333333333333,0.5333333333333333,0.7333333333333333,1.0,0.6666666666666666,0.23333333333333334,0.9,0.8333333333333334,0.8333333333333334,0.4666666666666667,0.5,0.26666666666666666,0.16666666666666666,0.9666666666666667,0.3333333333333333,0.1,0.1,0.0,0.06666666666666667,0.03333333333333333,0.0,0.0,0.0,0.06666666666666667,0.0,0.0,0.03333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.13333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.4666666666666667,0.0,0.0,0.0,0.0,0.03333333333333333,0.0,0.0,0.0,0.0,0.23333333333333334,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0)
gpt4_char_rare <- c(0.8,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.8666666666666667,1.0,0.7,1.0,0.6333333333333333,0.8,0.3333333333333333,0.6,0.13333333333333333,0.16666666666666666,0.13333333333333333,0.4,0.0,0.7,0.0,0.0,0.0,0.0,0.1,0.0,0.0,0.0,0.0,0.26666666666666666,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.26666666666666666,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.1)

# Llama 3
llama3_word_common <- c(1.0,1.0,1.0,0.9666666666666667,0.9,0.9666666666666667,0.9666666666666667,0.5666666666666667,0.3333333333333333,0.03333333333333333,0.16666666666666666,0.3,0.0,0.06666666666666667,0.3333333333333333,0.0,0.0,0.0,0.03333333333333333,0.06666666666666667,0.0,0.0,0.0,0.0,0.03333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
llama3_word_rare <- c(1.0,1.0,1.0,1.0,0.9,0.9666666666666667,0.9,0.7333333333333333,0.26666666666666666,0.03333333333333333,0.03333333333333333,0.03333333333333333,0.0,0.06666666666666667,0.1,0.0,0.0,0.03333333333333333,0.0,0.13333333333333333,0.0,0.0,0.0,0.0,0.03333333333333333,0.0,0.0,0.0,0.0,0.13333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.16666666666666666,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.03333333333333333)

llama3_char_common <- c(1.0,1.0,1.0,1.0,1.0,1.0,0.8666666666666667,0.9,0.9333333333333333,1.0,0.5666666666666667,1.0,0.16666666666666666,0.06666666666666667,0.9,0.43333333333333335,0.23333333333333334,0.0,0.0,1.0,0.0,0.0,0.0,0.03333333333333333,0.9,0.0,0.0,0.0,0.0,0.9666666666666667,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.7333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.23333333333333334,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.1)
llama3_char_rare <- c(1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.9666666666666667,0.4666666666666667,0.6666666666666666,0.2,1.0,0.5333333333333333,0.06666666666666667,0.6666666666666666,0.7,0.5333333333333333,0.7,0.0,1.0,0.0,0.0,0.0,0.0,0.9333333333333333,0.0,0.0,0.0,0.0,0.6666666666666666,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)

# Claude 3
claude3_word_common <- c(1.0,1.0,1.0,1.0,1.0,0.9,0.9666666666666667,0.9666666666666667,0.7333333333333333,0.8333333333333334,0.6666666666666666,0.8333333333333334,0.4666666666666667,0.3,0.7333333333333333,0.8,0.4666666666666667,0.7333333333333333,0.03333333333333333,1.0,0.1,0.6,0.03333333333333333,0.4,0.9666666666666667,0.1,0.06666666666666667,0.26666666666666666,0.0,0.9666666666666667,0.0,0.13333333333333333,0.0,0.0,0.5666666666666667,0.0,0.0,0.0,0.0,0.9333333333333333,0.0,0.03333333333333333,0.0,0.06666666666666667,0.26666666666666666,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.9,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8666666666666667,0.0,0.0,0.0,0.0,0.6,0.0,0.0,0.0,0.0,0.9333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0)
claude3_word_rare <- c(1.0,1.0,1.0,0.9666666666666667,0.9,0.8666666666666667,0.9333333333333333,0.9,0.9333333333333333,0.9333333333333333,0.6666666666666666,0.8333333333333334,0.4666666666666667,0.5333333333333333,0.7333333333333333,0.9333333333333333,0.3333333333333333,0.7,0.0,0.9666666666666667,0.0,0.26666666666666666,0.03333333333333333,0.36666666666666664,0.8666666666666667,0.0,0.0,0.2,0.0,0.9666666666666667,0.0,0.1,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.9,0.0,0.0,0.0,0.03333333333333333,0.3,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5333333333333333,0.0,0.0,0.0,0.0,0.6,0.0,0.0,0.0,0.0,0.8333333333333334,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0)

claude3_char_common <- c(1.0,1.0,0.9333333333333333,1.0,1.0,1.0,1.0,1.0,0.9666666666666667,1.0,0.9,0.9,0.9333333333333333,0.9333333333333333,0.9666666666666667,0.8666666666666667,0.6666666666666666,0.4,0.16666666666666666,0.8333333333333334,0.4666666666666667,0.7333333333333333,0.1,0.7,0.8,0.6666666666666666,0.2,0.4,0.0,0.7,0.03333333333333333,0.2,0.1,0.36666666666666664,0.3333333333333333,0.4666666666666667,0.43333333333333335,0.26666666666666666,0.03333333333333333,0.8666666666666667,0.16666666666666666,0.6666666666666666,0.3,0.5,0.6,0.4,0.1,0.5333333333333333,0.0,0.9666666666666667,0.16666666666666666,0.36666666666666664,0.0,0.23333333333333334,0.5,0.13333333333333333,0.0,0.0,0.0,1.0,0.0,0.0,0.03333333333333333,0.0,0.16666666666666666,0.0,0.0,0.0,0.06666666666666667,0.8666666666666667,0.26666666666666666,0.1,0.0,0.16666666666666666,0.03333333333333333,0.03333333333333333,0.0,0.0,0.0,0.1,0.5666666666666667,0.0,0.0,0.0,0.03333333333333333,0.0,0.06666666666666667,0.0,0.0,0.23333333333333334,0.03333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0)
claude3_char_rare <- c(1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.9,0.8666666666666667,0.8,1.0,0.7,1.0,0.5666666666666667,0.36666666666666664,0.7,0.8333333333333334,0.5,0.5,0.06666666666666667,0.9333333333333333,0.16666666666666666,1.0,0.0,0.5333333333333333,0.8666666666666667,0.13333333333333333,0.2,0.7,0.0,0.9333333333333333,0.0,0.23333333333333334,0.0,0.5666666666666667,0.26666666666666666,0.26666666666666666,0.1,0.0,0.0,1.0,0.0,0.0,0.26666666666666666,0.9,0.1,0.0,0.0,0.0,0.3333333333333333,0.5,0.0,0.43333333333333335,0.0,0.0,0.8666666666666667,0.2,0.0,0.0,0.0,0.7666666666666667,0.5666666666666667,0.0,0.0,0.43333333333333335,0.0,0.0,0.4,0.06666666666666667,0.0,0.6666666666666666,0.0,0.26666666666666666,0.16666666666666666,0.03333333333333333,0.1,0.0,0.0,0.0,0.0,1.0)

# Gemini
gemini_word_common <- c(1.0,1.0,1.0,0.8333333333333334,1.0,0.8333333333333334,0.9333333333333333,0.9666666666666667,0.9,0.9333333333333333,0.3333333333333333,0.23333333333333334,0.06666666666666667,0.13333333333333333,0.2,0.1,0.3,0.26666666666666666,0.36666666666666664,0.6333333333333333,0.1,0.06666666666666667,0.03333333333333333,0.06666666666666667,0.03333333333333333,0.0,0.0,0.0,0.0,0.4,0.0,0.0,0.0,0.0,0.1,0.0,0.0,0.0,0.03333333333333333,0.43333333333333335,0.0,0.0,0.0,0.0,0.13333333333333333,0.0,0.0,0.03333333333333333,0.0,0.6,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.16666666666666666)
gemini_word_rare <- c(1.0,1.0,1.0,0.8333333333333334,1.0,0.7333333333333333,0.9333333333333333,0.8666666666666667,0.8333333333333334,0.8666666666666667,0.23333333333333334,0.16666666666666666,0.0,0.06666666666666667,0.5,0.1,0.13333333333333333,0.06666666666666667,0.13333333333333333,0.7,0.03333333333333333,0.13333333333333333,0.0,0.03333333333333333,0.2,0.0,0.03333333333333333,0.0,0.0,0.5333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.6333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.4,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.03333333333333333)

gemini_char_common <- c(1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.9666666666666667,0.7333333333333333,1.0,0.36666666666666664,0.6,0.7,0.0,0.8666666666666667,0.9,0.06666666666666667,0.5,0.3,0.9333333333333333,0.6,0.1,0.5,0.1,0.5666666666666667,0.9,0.03333333333333333,0.03333333333333333,0.0,0.5333333333333333,0.0,0.6,0.0,0.0,0.0,0.6333333333333333,0.0,0.03333333333333333,0.0,0.7666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.26666666666666666,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.03333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0)
gemini_char_rare <- c(1.0,1.0,1.0,1.0,1.0,0.9666666666666667,1.0,0.9333333333333333,0.43333333333333335,1.0,0.4,0.3,0.8666666666666667,0.3333333333333333,0.9666666666666667,0.0,0.3,0.2,0.03333333333333333,0.8333333333333334,0.0,0.0,0.0,0.0,0.36666666666666664,0.0,0.0,0.0,0.0,0.23333333333333334,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8333333333333334)

# Olmo
olmo_word_common <- c(0.0,0.16666666666666666,0.1,0.0,0.0,0.0,0.0,0.0,0.1,0.0,0.0,0.0,0.0,0.8,0.03333333333333333,0.0,0.0,0.4,0.0,0.0,0.0,0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
olmo_word_rare <- c(0.03333333333333333,0.2,0.0,0.0,0.0,0.0,0.0,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.8666666666666667,0.0,0.03333333333333333,0.0,0.0,0.03333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)

olmo_char_common <- c(0.2,0.9666666666666667,0.5,0.16666666666666666,0.0,0.23333333333333334,0.0,0.26666666666666666,0.0,0.03333333333333333,0.0,0.13333333333333333,0.0,0.16666666666666666,0.06666666666666667,0.2,0.0,0.26666666666666666,0.03333333333333333,0.0,0.16666666666666666,0.26666666666666666,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
olmo_char_rare <- c(0.7,1.0,0.8666666666666667,0.3,0.26666666666666666,0.0,0.0,0.3333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.5333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)



positions <- 1:100
freqs_c4 <- c(-2.5124466705283957,-2.5170331521899887,-2.7399220364179215,-3.068885966138093,-2.9702881421816603,-3.391853547822746,-3.6018383328796904,-3.6269280539373674,-4.0140906304509265,-2.941671543014121,-4.095304539665636,-3.663787263306388,-4.299628286803836,-4.247460061348967,-3.67408731112318,-4.289925182154394,-4.5293862192784795,-4.1819273280206986,-4.649740174727181,-3.4402683131264795,-4.5746367866431985,-4.687883787063222,-4.843723978696567,-4.162226421020831,-3.9996495483138235,-4.846527957082268,-4.9371776672437795,-4.826062361540499,-5.087864073253836,-3.5153632121905165,-4.891960649641704,-5.27471251407096,-5.787040767721486,-5.852211503484272,-5.116708264927712,-5.532173036209542,-6.001315622527209,-5.946545188825845,-5.89826640283171,-4.293736385829477,-6.260122027658242,-5.876223956646963,-6.205006038593882,-6.0726545871092075,-5.219285589253746,-6.258549288146641,-6.341521023685292,-5.500012717529773,-6.2834776540353765,-3.897072809647429,-6.438255096653444,-6.217496833018417,-6.504341314333199,-6.424556252295282,-5.833887741018274,-6.411042533128559,-6.602065658400169,-6.517149039123107,-6.607248935462025,-4.535445996363713,-6.703004648800118,-6.482478900027987,-6.694867907407056,-6.06658344964095,-5.8091867727780215,-6.486418498032067,-6.6916316586278475,-6.712032202928339,-6.866870120773162,-5.061093219096826,-6.819868988939429,-6.148537479773772,-6.964878837296026,-6.8726616427527505,-5.478172490051472,-6.839341092352249,-6.917201414124522,-6.863986889559077,-6.948036333901529,-4.923162312594252,-6.918214072438907,-6.9202424707003,-6.992867747198259,-6.877513665857279,-6.240895662494949,-7.010489348548078,-6.976624834595322,-6.8544357185747335,-6.988510441829303,-4.873434249708151,-7.039803736216854,-6.921258214820136,-6.884346293707724,-7.071183417220334,-5.806516544222142,-6.76276159160333,-6.911146905215815,-6.6629672757402805,-6.120770772276923,-3.5511628309335355)
freqs <- c(1, 2, 3, 6, 5, 7, 11, 12, 17, 4, 18, 13, 24, 21, 14, 22, 25, 20, 28, 8, 27, 29, 31, 19, 16, 32, 36, 30, 38, 9, 34, 41, 45, 49, 39, 44, 53, 52, 51, 23, 62, 50, 58, 55, 40, 61, 64, 43, 63, 15, 67, 59, 70, 66, 48, 65, 72, 71, 73, 26, 77, 68, 76, 54, 47, 69, 75, 78, 84, 37, 80, 57, 94, 85, 42, 81, 89, 83, 93, 35, 90, 91, 97, 86, 60, 98, 95, 82, 96, 33, 99, 92, 87, 100, 46, 79, 88, 74, 56, 10)
freqs <- -1*freqs


cor(gpt35_word_common, positions, method="spearman")
cor(gpt35_word_common, freqs_c4, method="spearman")

cor(gpt4_word_common, positions, method="spearman")
cor(gpt4_word_common, freqs_c4, method="spearman")

cor(llama3_word_common, positions, method="spearman")
cor(llama3_word_common, freqs_c4, method="spearman")

cor(claude3_word_common, positions, method="spearman")
cor(claude3_word_common, freqs_c4, method="spearman")

cor(gemini_word_common, positions, method="spearman")
cor(gemini_word_common, freqs_c4, method="spearman")

cor(olmo_word_common, positions, method="spearman")
cor(olmo_word_common, freqs_c4, method="spearman")



cor(gpt35_char_common, positions, method="spearman")
cor(gpt35_char_common, freqs_c4, method="spearman")

cor(gpt4_char_common, positions, method="spearman")
cor(gpt4_char_common, freqs_c4, method="spearman")

cor(llama3_char_common, positions, method="spearman")
cor(llama3_char_common, freqs_c4, method="spearman")

cor(claude3_char_common, positions, method="spearman")
cor(claude3_char_common, freqs_c4, method="spearman")

cor(gemini_char_common, positions, method="spearman")
cor(gemini_char_common, freqs_c4, method="spearman")

cor(olmo_char_common, positions, method="spearman")
cor(olmo_char_common, freqs_c4, method="spearman")



counting_df <- data.frame(Accuracy=c(gpt4_word_common,gpt35_word_common,claude3_word_common,llama3_word_common,gemini_word_common,olmo_word_common,gpt4_char_common,gpt35_char_common,claude3_char_common,llama3_char_common,gemini_char_common,olmo_char_common),
                          StandardError=my_se(c(gpt4_word_common,gpt35_word_common,claude3_word_common,llama3_word_common,gemini_word_common,olmo_word_common,gpt4_char_common,gpt35_char_common,claude3_char_common,llama3_char_common,gemini_char_common,olmo_char_common), 30),
                          Type=rep(c("Word", "Character"), each=600),
                          Count=rep(positions,12),
                          Freq=rep(-1*freqs_c4,12),
                          Model=rep(rep(c("GPT-4", "GPT-3.5", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"), each=100), 2)
)


counting_df$Model <- factor(counting_df$Model, levels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"))
counting_df <- counting_df[counting_df$Model != "OLMo", ]

ggplot(data=counting_df, aes(x=Count, y=Accuracy, color=Model, shape=Model)) + 
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  geom_point() + 
  geom_line() +
  facet_grid(. ~ Type) + 
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20, 3), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  ylim(0.0,1.0) +
  scale_x_continuous(breaks=seq(0,100,10)) +
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank()) +
  labs(x="Magnitude of count", y="Accuracy")

ggsave("embers_0504_counting_acc_by_magnitude.pdf", width=12, height=4, dpi=100)


ggplot(data=counting_df, aes(x=Freq, y=Accuracy, color=Model, shape=Model)) + 
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  geom_point() + 
  geom_line() +
  facet_grid(. ~ Type) + 
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20, 3), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  ylim(0.0,1.0) +
  scale_x_continuous(breaks=seq(0,100,10)) +
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank()) +
  labs(x="Frequency of count", y="Accuracy")

ggsave("embers_0504_counting_acc_by_frequency.pdf", width=12, height=4, dpi=100)








counting_df_just_words <- counting_df[counting_df$Type == "Word",]
counting_df_just_words <- counting_df_just_words[counting_df_just_words$Model != "OLMo", ]
ggplot(data=counting_df_just_words, aes(x=Count, y=Accuracy, color=Model, shape=Model)) + 
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  geom_point() + 
  geom_line() +
  #facet_grid(. ~ Type) + 
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38"), labels=c("GPT-3.5      ", "GPT-4      ", "Claude 3     ", "Llama 3      ", "Gemini 1.0")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38"), labels=c("GPT-3.5      ", "GPT-4      ", "Claude 3     ", "Llama 3      ", "Gemini 1.0")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20), labels=c("GPT-3.5      ", "GPT-4      ", "Claude 3     ", "Llama 3      ", "Gemini 1.0")) +
  ylim(0.0,1.0) +
  scale_x_continuous(breaks=seq(0,100,10)) +
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank(),
        legend.margin=margin(c(-1,1,1,1))) +
  #theme(legend.position=c(0.86, 0.75)) +
  theme(legend.position="top") +
  labs(x="Number being counted to", y="Accuracy")

ggsave("embers_0504_counting_acc_by_magnitude_words.pdf", width=8.5, height=3.2, dpi=100)
ggsave("embers_0504_counting_acc_by_magnitude_words_tall.pdf", width=12, height=5, dpi=100)









accs_gpt35 <- c(0.003, 0.127, 0.138, 0.412)
accs_gpt4 <- c(0.028, 0.448, 0.069, 0.358)
accs_llama3 <- c(0.000, 0.003, 0.001, 0.253)
accs_claude3 <- c(0.050, 0.697, 0.135, 0.595)
accs_gemini1 <- c(0.025, 0.222, 0.062, 0.313)


counting_freq_df <- data.frame(Accuracy=c(accs_gpt35, accs_gpt4, accs_llama3, accs_claude3, accs_gemini1),
                               StandardError=my_se(c(accs_gpt35, accs_gpt4, accs_llama3, accs_claude3, accs_gemini1), 1200),
                               Model=rep(c("GPT-3.5", "GPT-4", "Llama 3", "Claude 3", "Gemini 1.0"), each=4),
                               Probability=rep(c("Low", "High"), 10),
                               Type=rep(rep(c("Counting\nwords", "Counting\ncharacters"), each=2), 5)
)
counting_freq_df$Probability <- factor(counting_freq_df$Probability, levels=c("Low", "High"))
counting_freq_df$Model <- factor(counting_freq_df$Model,levels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0"))

ggplot(data=counting_freq_df, aes(x=Probability, y=Accuracy, fill=Model, pattern=Probability)) + 
  geom_bar_pattern(stat="Identity", position=position_dodge(), color="black", , pattern_density=0.5, width=0.7) + 
  #scale_fill_manual(values = c("yellow2", "green3")) + 
  scale_pattern_manual(values = c("none", "none"))  +
  ylim(0.0,1.0) +
  facet_grid(Type ~ Model) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0")) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  theme(legend.position="none") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  #theme(axis.title.x=element_blank()) +
  geom_errorbar(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError), width=0.2,
                position=position_dodge(width=0.76)) +
  guides(pattern=guide_legend(title="Output\nprobability")) +
  labs(x="Output probability", y="Accuracy at counting") +
  theme(legend.key.size = unit(0.8, 'cm')) +
  guides(fill=guide_legend(title="Output\nprobability"))

ggsave("embers_0504_counting_acc_binary.pdf", width=6.5, height=4, dpi=100)




# words rare, words common, chars rare, chars common
accs_gpt35 <- c(0.143,0.127,0.219,0.338)
accs_gpt4 <- c(0.220,0.234,0.240,0.271)
accs_llama3 <- c(0.086, 0.087, 0.162, 0.172)
accs_claude3 <- c(0.250, 0.262, 0.508, 0.357)
accs_gemini1<- c(0.132, 0.144, 0.154, 0.222)


df_varyinp <- data.frame(Accuracy=c(accs_gpt35, accs_gpt4, accs_llama3, accs_claude3, accs_gemini1),
                         StandardError=my_se(c(accs_gpt35, accs_gpt4, accs_llama3, accs_claude3, accs_gemini1), 3000),
                         Model=rep(c("GPT-3.5", "GPT-4", "Llama 3", "Claude 3", "Gemini 1.0"), each=4),
                         Type=rep(rep(c("Counting\nwords", "Counting\ncharacters"), each=2), 5), 
                         InputProbability=rep(c("Low", "High"), 10)
)

df_varyinp$InputProbability <- factor(df_varyinp$InputProbability, levels=c("Low", "High"))
df_varyinp$Model <- factor(df_varyinp$Model,levels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0"))


ggplot(data=df_varyinp, aes(x=InputProbability, y=Accuracy, fill=Model, pattern=InputProbability)) + 
  geom_bar_pattern(stat="Identity", position=position_dodge(), color="black", , pattern_density=0.5, width=0.7) + 
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-3.5", "GPT-4", "Claude 3", "Llama 3", "Gemini 1.0")) +
  scale_pattern_manual(values = c("none", "none", "none", "none"))  +
  ylim(0.0,1.0) +
  facet_grid(Type ~ Model) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  theme(legend.position="none") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  #theme(axis.title.x=element_blank()) +
  theme(legend.key.size = unit(0.8, 'cm')) +
  labs(x="Input probability", y="Accuracy at counting") +
  geom_errorbar(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError), width=0.2,
                position=position_dodge(width=0.76)) +
  guides(pattern=guide_legend(title="Input\nprobability")) +
  guides(fill=guide_legend(title="Input\nprobability"))

ggsave("embers_0504_counting_acc_binary_inp.pdf", width=6.5, height=4, dpi=100)




















# NOT REVISED BELOW HERE




ggplot(data=counting_df, aes(x=Freq, y=Accuracy, color=Model, shape=Model)) + 
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  geom_point() + 
  geom_line() +
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#7CAE00"), labels=c("GPT-3.5", "GPT-4", "Llama 2", "PaLM 2")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#7CAE00"), labels=c("GPT-3.5", "GPT-4", "Llama 2", "PaLM 2")) +
  scale_shape_manual(values=c("circle","triangle", "square", "diamond"), labels=c("GPT-3.5", "GPT-4", "Llama 2", "PaLM 2")) +
  facet_grid(. ~ Type) + 
  ylim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.title=element_blank()) +
  labs(x="Negative log frequency of count", y="Accuracy")

ggsave("embers_1129_counting_acc_by_frequency.pdf", width=12, height=4, dpi=100)





# words_rare_common, words_common_common, chars_rare_common, chars_common_common,
accs_gpt35 <- c(0.003, 0.127, 0.138, 0.411)
accs_gpt4 <- c(0.028, 0.448, 0.069, 0.358)
accs_llama <- c(0.003, 0.004, 0.003, 0.018)
accs_palm <- c(0.032, 0.095, 0.005, 0.124)


counting_freq_df <- data.frame(Accuracy=c(accs_gpt35, accs_gpt4, accs_llama, accs_palm),
                               StandardError=my_se(c(accs_gpt35, accs_gpt4, accs_llama, accs_palm), 1200),
                               Model=rep(c("GPT-3.5", "GPT-4", "Llama 2", "PaLM 2"), each=4),
                               Probability=rep(c("Low", "High"), 8),
                               Type=rep(rep(c("Counting\nwords", "Counting\ncharacters"), each=2), 4)
)
counting_freq_df$Probability <- factor(counting_freq_df$Probability, levels=c("Low", "High"))

ggplot(data=counting_freq_df, aes(x=Probability, y=Accuracy, fill=Model, pattern=Probability)) + 
  geom_bar_pattern(stat="Identity", position=position_dodge(), color="black", , pattern_density=0.5, width=0.7) + 
  #scale_fill_manual(values = c("yellow2", "green3")) + 
  scale_pattern_manual(values = c("none", "none"))  +
  ylim(0.0,1.0) +
  facet_grid(Type ~ Model) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#7CAE00"), labels=c("GPT-3.5", "GPT-4", "Llama 2", "PaLM 2")) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  theme(legend.position="none") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  #theme(axis.title.x=element_blank()) +
  geom_errorbar(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError), width=0.2,
                position=position_dodge(width=0.76)) +
  guides(pattern=guide_legend(title="Output\nprobability")) +
  labs(x="Output probability", y="Accuracy at counting") +
  theme(legend.key.size = unit(0.8, 'cm')) +
  guides(fill=guide_legend(title="Output\nprobability"))

ggsave("embers_1129_counting_acc_binary.pdf", width=6.5, height=4, dpi=100)








# Varying input probability

# words rare, words common, chars rare, chars common
accs_gpt35 <- c(0.143,0.127,0.219,0.338)
accs_gpt4 <- c(0.220,0.234,0.240,0.271)
accs_llama <- c(0.047,0.062,0.049,0.053)
accs_palm <- c(0.100, 0.114, 0.067, 0.079)


df_varyinp <- data.frame(Accuracy=c(accs_gpt35, accs_gpt4, accs_llama, accs_palm),
                         StandardError=my_se(c(accs_gpt35, accs_gpt4, accs_llama, accs_palm), 3000),
                         Model=rep(c("GPT-3.5", "GPT-4", "Llama 2", "PaLM 2"), each=4),
                         Type=rep(rep(c("Counting\nwords", "Counting\ncharacters"), each=2), 4), 
                         InputProbability=rep(c("Low", "High"), 8)
)

df_varyinp$InputProbability <- factor(df_varyinp$InputProbability, levels=c("Low", "High"))

ggplot(data=df_varyinp, aes(x=InputProbability, y=Accuracy, fill=Model, pattern=InputProbability)) + 
  geom_bar_pattern(stat="Identity", position=position_dodge(), color="black", , pattern_density=0.5, width=0.7) + 
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#7CAE00")) +
  scale_pattern_manual(values = c("none", "none", "none", "none"))  +
  ylim(0.0,1.0) +
  facet_grid(Type ~ Model) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  theme(legend.position="none") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  #theme(axis.title.x=element_blank()) +
  theme(legend.key.size = unit(0.8, 'cm')) +
  labs(x="Input probability", y="Accuracy at counting") +
  geom_errorbar(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError), width=0.2,
                position=position_dodge(width=0.76)) +
  guides(pattern=guide_legend(title="Input\nprobability")) +
  guides(fill=guide_legend(title="Input\nprobability"))

ggsave("embers_1129_counting_acc_binary_inp.pdf", width=6.5, height=4, dpi=100)
















decoding_df <- data.frame(Logprob=rep(c(logprob_rev,logprob_pig,logprob_rot,logprob_swap,logprob_acronym), 2),
                          Accuracy=c(accs_gpt4_rev, accs_gpt4_pig, accs_gpt4_rot,accs_gpt4_swap,accs_gpt4_acronym,
                                     accs_gpt35_rev, accs_gpt35_pig, accs_gpt35_rot,accs_gpt35_swap,accs_gpt35_acronym,
                                     accs_claude3_rev, accs_claude3_pig, accs_claude3_rot,accs_claude3_swap,accs_claude3_acronym,
                                     accs_llama3_rev, accs_llama3_pig, accs_llama3_rot,accs_llama3_swap,accs_llama3_acronym,
                                     accs_geminipro_rev, accs_geminipro_pig, accs_geminipro_rot,accs_geminipro_swap,accs_geminipro_acronym,
                                     accs_olmo_rev, accs_olmo_pig, accs_olmo_rot,accs_olmo_swap,accs_olmo_acronym),
                          StandardError=c(my_se(c(accs_gpt4_rev, accs_gpt4_pig, accs_gpt4_rot, accs_gpt4_swap), 100), my_se(accs_gpt4_acronym, 1000),
                                          my_se(c(accs_gpt35_rev, accs_gpt35_pig, accs_gpt35_rot, accs_gpt35_swap), 100), my_se(accs_gpt35_acronym, 1000), 
                                          my_se(c(accs_claude3_rev, accs_claude3_pig, accs_claude3_rot, accs_claude3_swap), 100), my_se(accs_claude3_acronym, 1000),
                                          my_se(c(accs_llama3_rev, accs_llama3_pig, accs_llama3_rot, accs_llama3_swap), 100), my_se(accs_llama3_acronym, 1000),
                                          my_se(c(accs_geminipro_rev, accs_geminipro_pig, accs_geminipro_rot, accs_geminipro_swap), 100), my_se(accs_geminipro_acronym, 1000),
                                          my_se(c(accs_olmo_rev, accs_olmo_pig, accs_olmo_rot, accs_olmo_swap), 100), my_se(accs_olmo_acronym, 1000)),
                          Model=rep(c("GPT-4", "GPT-3.5", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"), each=17),
                          Task=rep(c(rep(c("Reversal", "Pig Latin", "Shift cipher", "Article swapping"), each=3), c("Acronym", "Acronym", "Acronym", "Acronym", "Acronym")), 6)
)

decoding_df$Task <- factor(decoding_df$Task, levels=c("Shift cipher", "Pig Latin", "Acronym", "Article swapping", "Reversal"))
decoding_df$Model <- factor(decoding_df$Model, levels=c("GPT-4", "GPT-3.5", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo"))



ggplot(data=decoding_df, aes(x=Logprob, y=Accuracy, color=Model, shape=Model)) + 
  geom_ribbon(aes(ymin=Accuracy-StandardError, ymax=Accuracy+StandardError, fill=Model), alpha=0.2, color=NA) +
  geom_point(size=5) + 
  geom_line(size=1.5) +
  ylim(0.0,1.0) +
  facet_grid(. ~ Task, scales="free") +
  scale_color_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-4", "GPT-3.5", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_fill_manual(values=c("#C77CFF", "#00BFC4", "#F8766D", "#B79F00", "#00BA38", "#619CFF"), labels=c("GPT-4", "GPT-3.5", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  scale_shape_manual(values=c(15, 17, 19, 18, 20, 3), labels=c("GPT-4", "GPT-3.5", "Claude 3", "Llama 3", "Gemini 1.0", "OLMo")) +
  #xlim(0.0,1.0) +
  #scale_x_continuous(breaks=seq(0,100,10)) +
  #theme(legend.position="top") +
  #guides(color=guide_legend(nrow=2,byrow=TRUE)) +
  #guides(linetype=guide_legend(nrow=2,byrow=TRUE)) +
  #theme(legend.key.width = grid::unit(3, "lines")) +
  theme(legend.key.size = unit(0.8, 'cm')) +
  #theme(axis.text.x = element_text(size = 11)) +
  theme(legend.title=element_blank()) +
  #theme(legend.position=c(0.915, 0.15)) +
  theme(legend.position="right") +
  theme(axis.text.x = element_text(size = 10)) +
  theme(legend.box.spacing = unit(0, "pt"), legend.spacing.x = unit(0, "pt"), legend.spacing.y = unit(0, "pt")) +
  #theme(axis.text.x = element_text(angle = 45, vjust = 1.0, hjust=1)) +
  #ggh4x::facetted_pos_scales(x = scales) +
  labs(x="Output log probability", y="Accuracy")





