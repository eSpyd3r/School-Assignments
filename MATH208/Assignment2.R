ggplot(heart_tbl, aes(x = RestingBP, group = Sex)) + geom_histogram(aes(y = after_stat(density), fill = Sex), col = "black", alpha = 0.4) + geom_density(linewidth = 1.0, adjust = 0.25, aes(col = Sex)) + xlab("RestingBP") + facet_grid(rows = vars(Sex))
#There appears to be little to no meaningful difference in distribution of resting blood pressure across the sexes.
#Both sexes have similar shapes in their density curves, and even peak at around the same values.
#Using only the historgrams and density curves, we can't say that theres an association between Sex and RestingBP
######Part 1.b
ggplot(heart_tbl, aes(x = RestingECG, group = ChestPainType, fill = ChestPainType)) + geom_histogram(stat = "count")
######

q1c_heart_tbl <- heart_tbl %>% group_by(Sex, ChestPainType) %>% summarise(n = n())%>% mutate(prop = n / sum(n))
q1c_heart_tbl
#Not sure what is meant by proportion, but my numbers for heart_tbl$prop are different than the example in the pdf

q1d_heart_tbl <- q1c_heart_tbl %>% pivot_wider(id_cols = ChestPainType, names_from = Sex, values_from = prop)
q1d_heart_tbl

####

q1e_heart_tbl <- heart_tbl %>% group_by(ChestPainType) %>% summarize_at(c("RestingBP", "Cholesterol", "FastingBS", "MaxHR"), list(mean=mean, median=median, IQR=IQR))
q1e_heart_tbl

####

q1f_heart_tbl <- q1e_heart_tbl %>% pivot_longer(cols=-ChestPainType) %>% pivot_wider(id_cols=name, names_from=ChestPainType, values_from=value)
q1f_heart_tbl


####

heart_tbl_modified <- heart_tbl %>% select(HeartDisease,RestingBP,Cholesterol,MaxHR) %>% mutate(HeartDisease=ifelse(HeartDisease==1,"Yes","No"))
heart_tbl_modified
q1g_heart_tbl <- heart_tbl_modified %>% pivot_longer(cols=-HeartDisease)
q1g_heart_tbl
ggplot(q1g_heart_tbl, aes(x=HeartDisease, y=value, group=HeartDisease, fill=HeartDisease)) + stat_boxplot(geom = "errorbar", width = 0.25) + geom_boxplot() + facet_wrap(~name)

########
#Q2
########

mig <- read_csv("GitProjects/School-Assignments/MATH208/migration.csv")
mig_sep <- separate(mig, Ref_Date, c("year", "month"), sep = "/")
mig_sep

###

mig_sep <- mig_sep %>% mutate(year = as.integer(year), month = as.integer(month))
mig_sep

###

mig_sep <- mig_sep %>% select(-Vector, -Coordinate) %>% filter(GEO != "Canada")
mig_sep
mig_summary_geo_int <- mig_sep %>% select(GEO, INT, Value) %>% group_by(GEO, INT) %>% summarize(sum = sum(Value)) %>% arrange(desc(sum))
mig_summary_geo_int
###

mig_summary_prov_total <- mig_summary_geo_int %>% pivot_wider(id_cols = GEO, names_from = INT, values_from = sum) %>% mutate(migrants_by_province = sum(`In-migrants`, `Out-migrants`))
mig_summary_prov_total

###

mig_summary_quebec <- mig_sep %>% filter(GEO == "Quebec") %>% group_by(year, INT) %>% summarize(mean=mean(Value))
mig_summary_quebec
ggplot(mig_summary_quebec, aes(x=year, y=mean, group=INT, col=INT)) + geom_line()

###

mig_sep_year <- mig_sep %>%  filter(year == 2002) %>% select(GEO, INT, Value) %>% group_by(GEO, INT) %>% summarize(Value = sum(Value)) %>% pivot_wider(id_cols = GEO, names_from = INT, values_from = Value)
mig_sep_year <- mig_sep_year %>% mutate(total = `In-migrants` + `Out-migrants`)
mig_sep_year <- mig_sep_year %>% select(GEO, `In-migrants`, `Out-migrants`, total) %>% ungroup()

mig_sep_year <- mig_sep_year %>% mutate(GEO = fct_reorder(GEO, total, .desc=TRUE))
mig_sep_year

ggplot(mig_sep_year, aes(x =  GEO, y = total, fill=GEO)) + geom_bar(stat="identity") + theme(axis.text.x = element_text(angle=90, hjust=1)) + xlab("GEO")



###

mig_sep_2002_quarter <- mig_sep %>% filter(year == 2002) %>% mutate( 
  quarter = case_when ( month == 3 ~ "1st",
                        month == 6 ~ "2nd",
                        month == 9 ~ "3rd",
                        month == 12 ~ "4th")
) %>% select(-month)
mig_sep_2002_quarter <- mig_sep_2002_quarter %>% select(GEO, INT, quarter, Value) %>% group_by(GEO, quarter) %>% summarize(total = sum(Value))
mig_sep_2002_quarter <- mig_sep_2002_quarter %>% ungroup()
mig_sep_2002_quarter <- mig_sep_2002_quarter %>% mutate(GEO = fct_relevel(GEO, levels(mig_sep_year$GEO))) %>% group_by(GEO, quarter, total)

ggplot(mig_sep_2002_quarter, aes(x = quarter, y = total, fill = GEO)) + geom_bar(stat = "identity") + ylab("Number of Migrants")



