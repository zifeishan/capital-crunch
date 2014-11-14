
<!--Potential investment match for tech companies -->

<!--Define the input-output behavior of the system and the scope of the project. What is your evaluation metric for success? Collect some preliminary data, and give concrete examples of inputs and outputs. Implement a baseline and an oracle and discuss the gap. What are the challenges? Which topics (e.g., search, MDPs, etc.) might be able to address those challenges (at a high-level, since we haven't covered any techniques in detail at this point)? Search the Internet for similar projects and mention the related work. You should basically have all the infrastructure (e.g., building a simulator, cleaning data) completed to do something interesting by now.-->

\begin{abstract}

For many start-ups, lack of investment and capital has become the
bottleneck for development. This phenomenon inspires us to use machine
learning algorithms to find patterns in investment behavior from major
investors. We propose to use various domain-specific features to predict
which investors would potentially invest in a particular company.
This would not only reveal important information about investment
strategies and behaviors of investors, but also give startups ideas on
where to seek potential investment and how to adjust their strategies
so as to attract potential investors.

Our work is grounded in CrunchBase, an accessible knowledge base that
maintains full records of company and people information.

There are two primary goals of our work:

(1) To predict whether an investor would invest in a particular start-up
based on textual, topological and domain-specific signals from both
the investor and start-up.

(2) To analyze and reveal the factors that would prompt an investor to
invest in startups so as to shed light on the adjustments the start-ups 
could make to attract more investments.

\end{abstract}

<!-- { Our goal is to infer investment events in technology companies using various domain-specific features. This work can potentially cast insights to understanding factors affecting investment behaviors, making strategies for companies and investors, and mining interesting patterns happening in the market. Our work is grounded in CrunchBase, an accessible knowledge base that maintains full records of company and people information.

We ask questions such as: what factors play the most critical role in investments? Can we infer whether an investor will invest a certain company by textual, topological and domain-specific signals?}
 -->


\keywords
{Machine Learning, Data Mining, Link Prediction, Probabilistic Inference, Startups}


# Dataset

We downloaded all the data from *CrunchBase.com*, one of the biggest databases about
information of companies. 

## Accessing data

CrunchBase provides indexing data and an API for full access of their
data. We requested the CrunchBase education plan API, which gives us a much
higher throughput when acquiring data, and we were able to get the full dataset.

The full CrunchBase dataset includes 214,290 companies and 286,659 people. We also parsed all known investments in CrunchBase, and got 31,942 investments.

# Approach

## Data Model

The CrunchBase dataset has a variety of entities: organization,
person, product, etc. There are also different relations
including investment, acquisition, degree, founder,
etc.

We currently focus on investment relationships.
For simplification, we categorize organizations into **startups**
and **investors**, and we care about predicting **investment**
relationship between them.

The data model is defined below:

- $Startup(startupId, [attributes...])$
- $Investor(investorId, [attributes...])$
- $Investment(investorId, startupId, isTrue)$

Where we use attributes (features) in $Startup$ and $Investor$ entities to predict
$Investment$ relations. 

## Problem definition

Our former problem is: 

\begin{definition}\label{def:problem}

Problem: given the full \textbf{Startup} relation and
\textbf{Investor} relation, predict \textbf{isTrue} value in
\textbf{Investment} table, which determines if any given investor
invests a startup.

\end{definition}

**The desired output** is a predicted probability between each investor and a startup.

<!-- ## Features

A rich set of features can be applied to predict investments. A list of features are described below:

- Start-up attributes:
  - Total funding used
  - 

- Company attributes. e.g. date founded, number of employees.
- Attributes of correlated people. e.g. degrees of founders and employees.
- Linguistic features: information buried in company descriptions and biography of people.
- Network topology, e.g. make use of all relations including degree, founder and other investments. These feature may be only captured by a factor graph model discussed later.
 -->

## Algorithm

In our initial model, we train an independent logistic regressor
for each individual investor, which takes a feature vector of a start-
up and predicts a label. 

The logistic regression model is a subcase of a factor graph model:
each $Investment$ relation is a boolean variable that we are
predicting, and the features are unary factors applied to variables.
The factor graph for logistic regression is demonstrated in Figure
\ref{fig:lr}. Each circle is a variable and each square is a unary
factor.  Note that the figure only represents the factor graph for a
certain investor. For each investor we train a model like this, and
their factor graphs are disconnected.

\begin{figure*}[t]
\centering
\includegraphics[width=0.6\textwidth]{img/logistic-regression.eps}
\caption{Logistic Regression model (for a single investor)}
\label{fig:lr}
\end{figure*}

The drawback of this model is that it cannot utilize investor-based
attributes and higher-level knowledge such as network topology.

As an improvement, we propose a factor graph / CRF model that correlates
features across this graph. In a factor graph, and features in both
sides of investors and startups can be correlated.

Figure \ref{fig:crf} presents a possible design of a factor graph model. In this design, we add a binary factor $f3$ to connect factor graphs:

A factor $Equal(I_1S_1, I_2S_2)$ is applied if $I_1$ and $I_2$ has a
common attribute $a_i$, and $S_1$ and $S_2$ has a common attribute
$a_s$, and the weight (coefficient) is determined by $(a_i, a_s)$.
Intuitively, **investors that have similar interest would prefer to
invest in similar startups,** and the degree is determined by the
specific attributes.

\begin{figure}[t]
\centering
\includegraphics[width=0.4\textwidth]{img/crf.eps}
\caption{Factor graph model that captures similarity}
\label{fig:crf}
\end{figure}

We use DeepDive \cite{zhang2014feature}, a highly scalable inference
engine to tackle the problem. L-1 regularization is applied during
weight learning, and Gibbs Sampling is used for inference.

## Features

A rich set of features can be applied to predict investments. A list
of features are described as below:

**Start-up attributes:**

- Unigrams (words) of short description of the start-up, with stopwords removed.
- Total funding used: we think the more funding the startup has used, the more promising it is and the more likely it will get another funding raise.
- Founded year: it is used combining with the total funding rounds. We use this to generate the negative example.
- Current team size: the size of founders in the start-up. We think the larger it is, the more likely it will be invested.
- Number of Competitors: we think the more competitors the start-up has, the less likely it will get the investment.
- Headquarters: the location of headquarters of the startup. We find that some specific VC likes to invest the startups in some specific areas.
- Category: the category of the service of the startup. We know that some VC are fond of the startups running on some certain kinds of service.
- Total items of websites: we think that the more official websites the startup, the startup are more likely to get the investment since websites are indicative of the marketing potential.

Note that in a logistic regression model, each investor will have
different weights (coefficients) for these different attributes. For
example, investor $A$ may prefer start-ups with headquarter in
Beijing, $B$ may prefer start-ups with larger team size, $C$ will
prefer start-ups in the category of artificial intelligence, etc.

**Investor attributes:**

- Total number of investments: if this investor has already invested more items, the more likely it gives a start-up investment under the same situation
- Total number of acquisitions: it is similar to the total investment items.
- Headquarters: the location of headquarters of the investor. It is similar to the feature of the startup's headquarter.
- Category: the category of the service of the investor. It is similar to the feature of the startup's category.

Note these features are not used in training independent logistic regressors, but they are useful in the full factor graph model.

## Getting training data

To train the predictor, we take ground truth investments in CrunchBase
as positive training examples, that is, if an investor $I$ has
invested in a startup $S$, we obtain a training example $(I, S, true)$
in $Investment$ relation.

For the negative training examples, it might not be desirable to
simply label all pairs of $(investor, startup)$ that do not have a
known investment as negative, because (1) this makes positive examples
extremely sparse and introduce a data skew, (2) this yields too many
training examples and makes training harder, and (3) even if an
investor have not invested a startup right now, it is still possible
that the investment will happen in the future. 

For now we sub-sample random pairs of investors and startups without known
investment happening as negative examples. In future work, we will apply
some heuristics to label negative examples. The proposed method is described below.

<!-- How to effectively
label negative examples is still open to us. For now we propose to
sub-sample random pairs of investors and startups without known
investment happening. -->

<!-- ### Generating negative examples -->

### Proposed heuristics for negative example generation

If a certain investor does not invest a startup, we cannot simply
label it as a negative example since there is a chance that this
investor will invest this startup in the future. Besides, there are
competitions between investors as the amount of investment for a
start-up is limited. If investor $A$ has made the investment for
startup $X$ but investor $B$ has not, we cannot say $(B, X)$ is a
negative example because $B$ may have the intention to invest $X$ but
$A$'s investment prevents it happening.

So we propose a model to help us generate the negative examples. For
all the startups, we have already known their founded year and funding
rounds. We believe that the longer this start-up exists and the less
funding rounds it has, the less likely it has the investment from
other investors and vice versa. Therefore we use this equation to give
startup X a probability to have negative examples:

$$P(X = N) = e^{-K}, K = \frac{\textbf{funding rounds}+1}{\textbf{running time}+1}$$

Intuitively, if the start-up has already run for a long time, it
should have more funding rounds. Otherwise, it will have a high
probability to get negative answers from investors. In contrast, if
the start-up only runs for a short time but has already got many
rounds of funding, it is very likely to get positive answers from
other investors. We add one to the numerator and denominator to smooth
it and also prevent illegal equation.


# Evaluation

## Evaluation metrics

We evaluate our models based on ground truth investments (positive examples) as well as randomly / heuristically labeled negative examples.
Specifically, we hold out a fraction of training examples, and use the predictions on these relations for evaluation.

We examine the calibration plots, where we layout
the predicted probabilities and the accuracy in test set in buckets. A discussion of interpreting
calibration plots is in the paper \cite{zhang2014feature}.

<!-- We may want to define our own measure to encourage aggressive predictions
and punish false negatives more than false positives. -->

We look at the accuracy of most confident predictions: we hope to
get a trained system where the most confident predictions are very
likely to be true. Specifically, we evaluate the precision where the system predicts a probability above $0.95$, as well as the recall.

We also evaluate the recall of predictions above probability $0.5$, as well as the recall.

We compare our results with a naive baseline model: a random predictor that predict random labels based on class priors. An oracle model would be one that knows
all existing investments and give correct predictions, which have precision and recall of $1.0$.

## Initial Results

We run experiments on a filtered dataset where each investor have at least 5 investments. We randomly label investor-startup pairs that do not have known investments as negative examples with probability of $0.01$. 
This yields a dataset of 9,521 positive examples, and 47,490 negative examples.

Factor graph size:

- 4.7 million variables
- 115 million factors
- 3.1 million different weights

Calibration plot: See Figure \ref{fig:calibration}.

\begin{figure*}[t]
\centering
\includegraphics[width=0.9\textwidth]{img/calibration.png}
\caption{Calibration plot for investment predictions}
\label{fig:calibration}
\end{figure*}

High confidence (probability $>0.95$ predictions):

- Precision $81.22\%$ (over labeled data)
- Precision $0.91\%$ (if count all predicted unlabeled data as false positives)
- Recall $3.13\%$ (over all 2460 held-out positive examples)

Half confidence (probability $>0.5$ predictions):

- Precision $59.34\%$ (over labeled data)
- Precision $0.37\%$ (if count all predicted unlabeled data as false positives)
- Recall $40.7\%$ (over all 2460 held-out positive examples)

<!-- 
crunchbase=# select is_true, count(*) from investment_is_true_inference group by is_true;
 is_true |  count
---------+---------
 t       |    2460
         | 4672511
 f       |   11809
(3 rows)

crunchbase=# select is_true, count(*) from investment_is_true_inference where expectation > 0.95 group by is_true;
 is_true | count
---------+-------
         | 36140
 f       |    77
 t       |   333
(3 rows)


crunchbase=# select is_true, count(*) from investment_is_true_inference where expectation > 0.5 group by is_true;
 is_true | count
---------+--------
 t       |   1003
         | 270050
 f       |    687
(3 rows)
 -->


## Initial error analysis

The results are not optimal. Specifically, we see severe underfitting from the calibration plot. Possible reasons include unexpressive features or models, or bad labeling strategy. We will discuss improvements in future work.

## Result analysis

Here is a list of top indicative features for the investor *Sequoia Capital*:

- headquarter=Shanghai
- headquarter=Beijing
- num_websites==5
- num_competitors==2
- category=Web Hosting
- founded_on_year=2005
- short_bio_1gram=services
- num_websites==4
- headquarter=Houston
- num_competitors==10
- founded_on_year=2004
- category=Databases
- headquarter=Pune
- category=Technology

We see some interesting results in these features: this investor
prefers Asia startups, in field of web hosting, services, databases
and technology. 

Analysis like this might help startups find ideal investors, making
marketing strategy and technical decisions.

# Future Work

We clearly see several directions of improvements towards a better predictor:


(1) Improve features. We will add textual features in company descriptions, rather than using simple unigrams of short-bio. We have already parsed all the sentences in company descriptions using Stanford CoreNLP. We have also downloaded information about startup founders, which might help improving features.

(2) Improve models.  We will add the similarity CRF rule discussed above, and propose more expressive rules such as people-related rules, or propose HITS/PageRank-like models (good investors invest in good startups, and vise versa), whose idea is similar with a previous work discussed in \cite{shan2012gamerank}.

(3) improve supervision methods. We should integrate the heuristics of generating negative examples discussed above. Further questions include: how many negative examples to generate? How to do proper train/test split? Specifically, we might hold out start-ups, rather than single investment edges.


<!-- We want to use the information from people and organizations, finding
the connections, common points and all the relationship we can get
from the data to learn a graph. Using this graph, we want to predict
the probability of the investors a company, and what kind of
investors, which exactly investor will invest on a certain kind of
company. The data we get from crunchbase will be separated into two
parts: training and testing, to help us evaluate the behavior of our
model and help us chose good predictors and relationship between nodes
(including people and organizations). Therefore we could evaluate if
our model is trained well and use the information we get properly.
 -->

<!-- 
# Challenges

We see several challenges in the project:

**Data sparsity.**  To predict pairwise investment relationship
between investors and startups, training data might be very sparse and
highly skewed: most investors only invest a few companies. We may
reduce feature space by carefully engineering features through error
analysis, or trying methods like SVD. More advanced models, e.g.
collaborative filtering, or a joint inference model that correlates
prediction on all investors, would also help tackling the sparsity
issue.

**Feature extraction.** Designing and extracting features are the key
to a successful predictor. To fully utilize the information hidden
from raw text such as company descriptions and founder bios, we
propose to adopt state-of-the-art natural language processing methods
for feature extraction, including named entity recognition and
dependency parse.

**Model high-level knowledge.**
Some high-level knowledge would be hard to capture by a simple
logistic regression model. We propose to use factor graphs to model
the correlations between different investors, company and people, etc.

**Scalability.**
If we are building a factor graph model with a large feature space, it
would be hard to do learning and inference on the graph. We propose to
use DeepDive \cite{zhang2014feature}, a highly scalable inference
engine to tackle the problem.

**Future extensions.**
If time permits, we might extend our model to predict company
acquisition in this dataset. We also propose to do analysis on
important factors in investment and acquisition behaviors.
-->

# Related Work

In the paper \cite{an2014recommending}, the author discussed a
methodology to match proposals from start-ups to the potential
investors on Kickstarter with linear regression, SVM-linear, SVM-poly
and SVM-RBF, with an accuracy rate of 82% for static data features and
73% for dynamic data features. Their features are mostly updates made
to the tweets, number of comments and so on, and we could widely
expand the feature set.

Another paper \cite{gartner1999predicting} used a discriminant
analysis to classify the potentially successful and unsuccessful
companies. Their feature sets are worth noting, including individual
characteristics of the entrepreneurs, the efforts by entrepreneurs
(i.e. whether they actively look for resources and help), degree of
innovation and so on. Though this paper is more on the social science
side, we would like to scrutinize the feature sets so as to explore
more meaningful and insightful features. For example, we could extend
individual characteristics to how many start-ups the CEO has founded
and their histories.

