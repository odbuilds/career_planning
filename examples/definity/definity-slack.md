Nipuna  [11:02 PM]
Workshop w/ Deloitte Team, John, Nipuna -- June 6th

TLDR: Good workshop covering the basics for key issue use case and a slower walkthrough of tool.

Put my entire notes below on each use cases and ideation around dataset/setup
Since everything is via API's I need to spend more time with them to get a good grasp before next week. 
Their prepping some mock data to have before next week. 
MSA in progress from Definity team and no major blockers 
Overall good start and next week have two calls to explore more around the last two use cases.


----
Covered

Prompt for key issue extraction with Google Gemini, and Prompts and Pipelines basics
Second workspace uploaded as unlabelled data --> Build model with Divide and Conquer 
Training and evaluation, finding model gaps/confusion with metrics


Key Notes

Key-Issue Topic Modelling

Model Build: Conversations --> Pipeline of key issue summaries with Gemini --> Build Topic Model with HF
Prod: Bring in conversations into separate workspace --> Use Pipelines via API to Extract Key Issue --> Take Payload and BatchPredict call to HF NLU Model --> Get results --> Agent Self-Serve Missed Reasoning Pipeline --> Output
Agent Self-Serve Missed Reasoning is "find hints of why Agent/Customer had to call in instead of self-serve (website, chat, other options)". 
They want to run this at the end and would be a seperate prompt/pipeline after getting the labelled prediction.



FAQ Extraction

Dataset is a flat list of FAQ questions from Definity (not answer units)
Want to categorize them (auto insurance, home insurance). Also extract questions customers asked in calls and find if those are not well covered in the original list

Proposed build a category model from the flat list of questions --> Pipeline to extract questions customer asked for --> Predict call to model to see where the question fits and if its covered based on a certain confidence threshold
Not sure if this is the best way to do that -- they didn't seem to propose alternatives either? 



Senior Agent Escalation

Initial agent unable to resolve that issue --> initial agent is asking/contacting senior agent advice how to resolve the issue
Goal is to identify why are those escalations happening (what do the agents not have, are they missing any knowledge base, experience or lacking confidence) 
There exists some business logic that indicates whether an escalation happened so that doesn't need to be identified
Need to figure this out based on the mock data they provide TBD


Callback Analysis

Customers where the initial call didn't resolve the issue and customer are calling in again
Business logic should exist to identify if its a callback
Trying to use policy number  data field + calling period within 5-7 days + same key issue to identify repeat callers without looking into customer data initially

Need to figure this out based on the mock data they provide TBD




Questions Raised


When using batch predict against the model with API -- how can model drift be tracked
"Once you have model and are calling API via Prod application, does that data get stored somewhere with the predictions?
Ex. Is there a rolling JSON of last couple months of predictions? does that get stored in the tool when calling the API or is it a manual upload"
Verified its two different steps (first apply Pipeline) then batchPredict -- however need to store the batchPredict results over time period on the UI somewhere -- need to check if that happens automatically or its a third step to upload into a workspace somewhere
Guessing can configure own rolling window of data in a separate workspace to have for client to access to track model drift as a separate step from the batchPredict -- Maxime (deloitte team) would be responsible to setup that continuous data upload pipeline through the data window.
How to configure a rolling window for datasets to help the client track uncovered / model drift by themselves in the UI



2. What is the testing strategy within the tool -- Once the 4 pipelines/model is built, strategizing ahead, Definity may provide test data with metadata containing ground truth. How can we verify model outputs against that within the tool?

What is the process of checking the model outputs against that ground truth. 
Is there a process within tool to do that testing or is it a manual check or custom script?
Guessing this will be complicated and a multi-step process different for each use case
Ex for key issue --> first generate the key issue summaries, upload as Unlabelled, run training on that, download as CSV and then compare topMatchIntent to groundTruth metadata field??



Next Steps (Two calls next week -- Tue/Thur 2:30pm-3:30pm EST)

Discuss the other two use cases (Senior Agent Escalation/Callback Analysis) and strategize on testing
Deloitte team trying to come up with mock data based on data dictionary  (variables and metadata fields chosen to be used)
Trying to come up with 10 mock records and will be checking with Definity to see if its ok to share before the next call.

Want to know what the outputs look like, where it can be exported, how to do the testing with ground truth and how to evaluate the model
I'm going to get familiar with using the API as much as possible to setup something like the key-issue pipeline so I have a better idea of describing this to them.
Stephen  [3:18 PM]
OK - finally got my notes out and the environment setup.
Have chased MSA etc - this is really useful Nipuna above.
I don't know whether we will be able to get enough time to answer some of these questions as really low level - we can see if can fit a call.
Otherwise I think there is enough to just onboard them onto tool and practically start in the session - they can start pushing up and down, looking at APIs etc.

It's nice they are doing all this advanced thinking but without MSA + Data it's completely moot. (edited) 
Stephen  [4:13 PM]
Hi @Nipuna the testing question seems very involved.
I think it would be helpful for us both to be on to answer it and have some prep time.[4:13 PM]Shall we push back the meeting today till the Thursday one.
Nipuna  [4:14 PM]
Yes sure I can email Urvashi and let her know we will push it back to Thursday
[4:15 PM]I think that would be best b/c this is a pretty complex workflow between all four of the use cases
Nipuna  [4:25 PM]
Fayaz walked me through the test set feature in Evaluations, and merging a Excel sheet model (utterance/label) into the model workspace, attaching a tag and then using that in the evaluation run. However, they are likely to follow up with more questions specific to the use case.
I will push the meeting back to Thursday then @Stephen?
Stephen  [4:26 PM]
Please push back
Nipuna  [5:14 PM]
@Stephen They're insisting due to crunched timelines they want to have the session today to ask questions and review the mock data.

Happy to run a simple session for today. I had an example prepared for today of using the hf-module and APIs to get out a Key Issue visual in a Juypter Notebook which I can go over to give them an idea on the objects returned and provide more familiarity with API. I can go through with that as an informative session and leave the questions regarding testing for Thursday. Does that sound ok?
Stephen  [7:26 PM]
Nice work.  Please push any testing questions till THursday - concentrate on upskilling deloitte on the resuable HF functionality.
[7:26 PM]The back is the that Definity haven't signed the deal yet, we should not be doing project specific work yet.
Stephen  [7:47 PM]
Sent a email giving you some coverage for that.  Thanks for having a proactice session ready, if they are asking arkward things feel free to capture them and just push everythign to Thursday when I can be on.
Nipuna  [7:48 PM]
Sounds good thanks!
Nipuna  [10:44 PM]
June 11th -- Call w/ Urvashi, Riddhi, Stephen (BI team responsible for Tableau portion)

TLDR

Got a good view on the dataset their getting -- relevant fields and screenshots attached. Think they need some time to share even the mock data with us or upload to workspace (probably waiting for contract stuff)
They really like the end to end workflow with the HF API I showed with a notebook to visual -- requested the notebook and mentioned Riddhi will play around with it
Workflow was JSON file --> Create Conversation Set --> Link --> Run Pipeline --> QueryPipelineOutput --> Extract Utterance Texts --> BatchPredict to Prod Model Workspace --> Map back data to original pipeline output --> Visualize as Pie Chart
Shared the notebook via email and the sample JSON files generated for the ABCD example

Next steps a few things to follow up on Thursday and testing strategies while we wait for the contracting / data stuff to go through


Mock Data (screenshots attached)

Went through the mock data and data dictionary prepared
LOB Sonnet (broker) | NBS (customer) <> Language English | French <> Channel Chat | Call
Call data set contains: (ids, timestamps, role, sessionID, call duration, transcript [for each utterance startTimeSeconds, endTimeSeconds, utterance, speakerID, speakerRole], campaign_name [identifies whether Sonnet or NBS] )
Here the timestamps are in seconds and not a dateTimestamp -- mentioned she can probably use the startTimestamp in Call Segment CSV to map each utterance if needed

Call Metadata -- two seperate CSVs -- Call Segment CSV and Call Log CSV
Call Segment CSV -- Useful for Senior Agent Escalation usecase -- (Call_ids, Segment Type Skill Transfer, Incoming Call, Transfer to 3rd party )
 Call Log CSV -- (Call_ids, date_timestamp, only useful one here is Call_Type Inbound | Outbound )

Chat CSV + Metadata picture attached
Useful fields are Omni.subject (contains the main reason customer mentioned to bot need assistance about) and Omni.question (contains the full transcript from bot to agent if needed)
Not doing bot -> agent reasons for Senior Agent Escalation usecase -- only call logs



Questions To Follow Up On Thursday

Testing around ground truth and testing strategies --> didn't go over anything here and both Urvashi/Riddhi will ask q's on Thursday
How to connect other embedding models --> Only Universal in the dropdown
Mentioned we can follow up on this
They don't have a specific model in mind to try -- just evaluating to ensure the best one is chosen for the client
Can go over on Thursday since I didn't know how custom embedding models are enabled

Shed more light into BigQuery Integration
Their pipeline wise --> Ingesting the relevant data fields in those CSVs to BigQuery 
Can we bring data in directly from bigQuery --> Answered yes but I mentioned the feature was fresh and coming up soon. I tried to show the BigQuery in Integrations but the logo wasn't there so mentioned we can provide more input on that next Thursday
This will let them skip the convert to JSON step which is a big value add for them as they mentioned

What would change with a mock French dataset compared to English? Would anything need to change in the pipeline? If the client requests two models one for french/english then what would the process be?
Confirmed --> The headers and all fields will stay the same in the French dataset --> Only difference is the language uttered
Mentioned since the embedding model is agnostic and headers and data format stays the same, it should work fine regardless french or english
To follow up on thursday --> Guessing only if the client requests two seperate models would they need to build two different ones?


Embeddings.
You need to create a namespace for each embedding you want to try out setting it up like this.

Generally if you are using chatbot style utterancs - like a short sentence, USE is very good and there is very little advantageis  going up from there.  If your generated results or input docs are bigger though there is advantage going up.

Mini X
Then if you ask AP or Matt they can add mini llm v6 and v12 and select from drop down.    LLM v6 particularly good with review or answer chunk like data.  lFor OpenAi you need to look up

OpenAI
You have to look up the model name on the opena i page, then add it ot the "Models" tab of your integration (where you added the key).  Warning, if your documents are really really long it gets overly onerous.  THe embedding only work up to 8192

Co:here
you have to add the model name and like openai, but you also have to specify the /embeddings as part of the end point - there is a jira ticket trying to expand the docs to cover.

You can try it out on ABCD here https://studio.humanfirst.ai/organization/user-management?namespace=academy


Stephen  [4:56 PM]
Spent a couple of hours on prep

Notebook complete and easy using humanfirst - Deloitte have it and can make progress.  Couple of niggle functions we didn't have.  Stephen - try and clear the work in PR, after that we'll review if a gap and can add on the two extra.
practiced blindset testing strategy end to end - will make a good demo today.
practiced bigquery on staging - will be very useful for - going to demo today, but have issues we need to address separately at cowork
is it released?
timestamps data type are not processed - workaround to cast them as unix_timestamps in SQL
permissions - admin bigquery sounds wide - what do we actually need.

fr/en recommend they work in en but tell prompts the conversations could be fr/en and ask for en output.  If they do need two prompts into two models then can help them by bootstrapping fr from en or vice versa.  Then letting maintain joint or separate models


June 13th -- Call w/ Urvashi, Riddhi, Maxime, Steven (Deloitte) - Stephen/Nipuna (HF)

Project Timelines
Deloitte are responsibile for the orchestration of everything and getting client end result of dashboards
June 25th is their timeline deadline to have SSO and everything setup so they can bring real data in and not work with mock data -- has been communicated to Definity.

Walked through blindset testing workflow within tool
Their planning on doing a fixed topic modelling custom beforehand and use HF as the last step for prediction.
Image attached for their choice -- mostly a prompt extraction problem to extract multiple key issues each as a sentence? -- TBD on their plans

Covered mock data they currently have available
Successfully used the script to convert to HF JSON and have the mock data uploaded within the tool
Chat log data confirmed to be converted into conversation format as well instead of a single text

Showcased BigQuery integration
Showed process of importing data into a workspace from BigQuery
They confirmed very happy to see and data format would look similar
Need to verify API usage around BigQuery

LLM Model discussion
Fixed on using Gemini -- want to use 1.5-pro or the bigger models for the "thought" based prompts
Recommended ensuring rate limits are increased. RPMs 

French<>English dataset discussion
Nothing specific from the client -- Currently choosing to keep English only and have the prompt step handle the extraction into English



Next Steps:

(DONE) Provide Vertex Loan key so Riddhi is unblocked with prompting work
Service account created seperately for definity-deloitte in hf-clients-df GCP

Ask backend team to enable other embedding model in namespace  namespace=definity-definity-embedding-model
Verify API usage to trigger BigQuery Conversation Link / Import
On their side:
Urvashi to check contract details to confirm Deloitte is signed work agreement


June 20th -- Call w/ Urvashi, Riddhi, Maxime, Steven (Deloitte) - Stephen/Nipuna (HF)

TLDR: Moving smoothly. Data pipeline from Deloitte side internally still being worked out between BigQuery and HF JSON. Aiming for June 25th to get actual data in. Deloitte team is well equipped with how HF interacts and how the pipeline will run.


Covered setting up PROD, QA workspaces in the main namespace (revisions, exporting reports, merging back to dev)
Access to BigQuery tables via ServiceAccount (Data Security)
They have service key -- wondering what tables HF would have access to with that.
Mentioned whatever tables the service account has perms for will be accessible within HF
Team to re-route on that

Tableau demo for Key Issue completed -- helped Steven (BI - Deloitte team) feel more comfortable with how the data would come in
Most of BI Steven's concern sit around how the data will look but these are not really dependent on HF and more so on their data pipeline
Final data to be annotated will be the raw conversations themselves (key PK is convoID)
Confirmed to him that he wouldn't need to be dealing with HF JSON and will just have direct access to BigQuery tables

Recommended to bring in conversation sets via API vs BigQuery integration with HF due to need for consistent rolling ingestion
Want to ingest bulk set of calls every hour or so new conversations to keep up to date
This way one convo-set can contain a days worth of conversations ingested each hr
They are responsible to setup the conversion to HF JSON through the pipeline -- since initial planning was around using BigQuery <> HF direct they will re-route and come back.

FAQ Extraction Discussion
Deloitte expecting classification for questions extracted from convo as Verbatim, Lightly Inferred, Heavily Inferred
Stephen suggested against this due to variability with LLMs - they mentioned aligned
Concurred that current test data set would be great as a blindset test but don't rely on that
Also that the classes currently defined might not be the classes that actually exist




To-Do's:

Address and emails provided for contracts and laptops (DONE)
Deloitte to rethink/discuss the FAQ extraction piece and HF JSON conversion via pipeline removing BQ
Will play around with the FAQ prompt idea and test results to see similar to what they are expecting


June 25th Call -- Call w/ Urvashi, Riddhi, Steven (Deloitte) - Nipuna (HF)

[Security / Contract / Environment]

Asked if they would setup Teams communication channels since Slack isn't an option
They mentioned sending a laptop with a Deloitte email which then would allow for comms through that and not via invites to our HF emails

Q on environment raised: Would the environment for Definity be different from our regular cloud environment. 
My understanding is that its our regular cloud prod environment, however access to calling APIs is done privately and is not a case of an "on-prem" deployment.
They raised due to worries that me/Stephen won't have access but mentioned that can be resolved.  Something to clarify on Thursday's call



[Timelines]

Aug 16th is Go Live data for FAQ extraction
Sept 6th is Go Live data for remaining three use cases


[FAQ Extraction Use Case]

They have moved to using 3 separate prompts for verbatim, inferred from the client, inferred from the agent  and are passing the full context conversation each time. Model choice is gemini-pro-1.5
Definity wants to know these categories

Prompts are very basic and just the first iteration some are extracting like 20-30 questions at once.
Currently running in Jupyter Notebook on real scrubbed data but cannot do any real prompt tuning.
Mentioned to Riddhi that the prompt tuning can be done easily once the data is in HF and they are looking forward to that.

Q on how to tag the prompt output with one of those three classes so mentioned to use the pipelineID corresponding to the prompt which won't change


[FAQ Model]

Used for second step in FAQ extraction flow of topic modelling the extraction question
To build model they have a simple FAQ taxonomy for sonnet and will get provided one for NBS
Super simple parent/child taxonomy so mentioned will likely need to do divide-n-conquer seperate

Q raised was how much utterances / FAQs to label for the model - showed training and coverage metrics we provide which they were very pleased with.
Showcased sample workspace with divide-n-conquer ABCD FAQ model and API end to end workflow from extraction to batch predict
Showed the variability I saw in testing in using inferred, lightly and heavily which they aligned on



[Next Steps]

Call Thursday to work out final details on environment, data import, ect with Definity folks 
Continuing help around ideation while waiting for real data -- Probably look at improving their prompts and continuing to ideate on pipeline


Started chain in teams
Something to note : While converting actual data ( as opposed to Mock Data ) , I noted that `participant_role` column can take IVR ( Robot ) or UNKNOWN ( where neither Agent nor Customer is inferred from the transcript ). For the time being, I made script changes to put IVR as Expert and UNKNOWN as Customer. I look forward to discussing this with you and hearing your advice in our next meeting. Dasani, Riddhi currently there is client or expert supported for every utterance. If you are unsure based on transcription you need to decide which one you err on the side of. If you'd like an unknown role in the future we can look to include it with a feature request here https://zia-ai.atlassian.net/servicedesk/customer/portal/1[3:15 PM]Authentication for APIs.

So recapping what Mathieu covered.

Authentication for apis is via a Bearer Token, that you get via the standard Google Identify service using a Username/Password
You then pass that Bearer Token in teh header in the standard way and refresh it when it comes up to expire using the refresh token.
This you can do manually using this explainer
https://docs.humanfirst.ai/docs/api

As you can't use your SSO username/password for this, Mathieu is going to create a separate backend configured service account username/password (see actions)

Once we have this - how to use.

To save you having to do this there is the pypi module which manages all this for you. (import humanfirst)
https://github.com/zia-ai/humanfirst-module/blob/master/humanfirst/apis.py#L825

This supports three ways of passing the username/password to get the api connected

Environment variables (Recommended)
export HF_USERNAME and HF_PASSWORD and the code will check for it.
if you are within a cloud environment it would be good practice to manage these in a secret manager (like Google Secret Manager)

.env file (convenient for local development)
This could be read from a secure google drive or storage bucket - but probably not the best way in a cloud environment, but it's convenient when doing local dev.

Pass the username/password as arguments to the function (not recommended unless you store the password securely somehow)
Storing the password in your script in plain text not recommended.
But if you have a way of bringing in securely as a variable this is available to pass.


Stephen  [9:31 PM]
~100 datpoints uploaded, issues with roles/timestamps.
Some loading discrepancy between vertex studio results and hf - debug when reloaded roles.
Very good questions from Riddhi
Urvashi looking a bit worried on progress/speed? - but felt like we were making good progress.
Deloitte seem to be behind on their data gathering
Highlighted they need at leaset 10,000 conversations to get any meaningful result for a 100 class model.
Ideally they want a full timeperiod, like a day or a week.

Actions

Sreekar: admin level bump groups for all users running prompt

Riddhi download CSV and share via Stephen Deloitte account - Stephen/Nipuna reconcile
 number in CSV v number in HF via SQL load

SQL changes
 unix_timestamp casting
 role mapping with translation table

Tuesday: faq prompt 1-4 faqs expected, faq grounded/evidancy prompt and key issue prompt.


Stephen  [9:18 PM]
Just been mulling something across Epinions and Definity.

Prior to JSON mode being available, I think it's really hard to work in JSON in tool, and I'm suggesting flipping back to Key-Value pairs for these two projects.

The splitting seems to be much more durable and it's much easier to read in tool and use batch actions.  I presume it's splitting on the actual "^key_name:[\s]+" so is tolerant of the other line breaks etc (it seems freinedly)
Even dropping to python and using the json_format mode just meant when it hallucinated it hallucinated JSON.  Things like this (note the comment into a key name)

{'review_id': '61ec7ed9772ec04536ad', 'item_code': 'elec-Video-DVD-All-Sony_DVP-S360', 'date_drafted': '2024-07-01T18:28:48.625136', 'stars_rating': 4, 'amount_paid: 299.00 USD,  # Fixed a slight formating issue here with the correct input type and value for amount paid. The ': ' has to be fixed the same way as. The closing bracket Formats as fixeable or use them as inline suggestion in the following format. I have als

Overall valid
False        828
True       13998
~ 6% invalid to JSON schema.

Whilst we could burn more time trying to get functions going and try and validate that fixes it - I feel like it's taking us further and further away from what we can do in tool.

@Nipuna - something to think about for Definity urgently - I think working in JSON now may be a mistake.  Working in key-value produces more robust outputs and easier to isnpect qualitgy.  Can flip to JSON when a feature easily from that.

@seb @mathieu heads up that JSON mode may be harder to get the results into batch - getting a lot of weird keys, missing keys, valid but not requested keys, comments.  Whilst it doesn't show up on a 10-20 sample, when you get into the thousands it's an isue.

SS of nicely format key pairs.
This WS
https://studio.humanfirst.ai/playbooks/playbook-F3IA4N77WJDXXP23IDC6URLL/explore/uttera[…]BYNSSL&stashId=P97813h45EQRG25089234t5&showDuplicates=true


Initial Prompt Testing Results for FAQ Extraction Prompts

Tested on small sample of 5 full conversations 
Tested 3 Separate Prompts vs Single Prompt With Classes vs Single Prompt Without Classes
Model Gemini-1.5-Pro, outputting as JSON markdown array object, temperature 0


Variability with temperature 0

Tested same prompt at temperature zero with 4 separate runs and compared to original run
Gemini at temperature zero without any prompt changes seems to consistently produce the same exact output each time


Single Prompt With Classes

Currently seems to be the best working one and tends to interpret FAQ questions into the correct classes properly
Sometimes provides more information than necessary but much less likely than 3 separate prompts


Single Prompt Without Classes (Pure FAQ)

Does decently as well — questions seem to be more personalized. 
More tuning can likely get this performing well as well so viable option to explore.
Running a second prompt for classification of outputs is yet to be tested but could also be a good combo.


Three Separate Prompts

Tend to end up with a lot more extra information/descriptions
Perhaps forcing to pull out MAX of 2 questions will avoid this behaviour.

Tends to have high repetition of re-worded question between Verbatim and User Inferred
Tends to be missing context and just extracting pure questions without considering overall conversation


Prompts are in this workspace --> https://studio.humanfirst.ai/playbooks/playbook-3M4PCNCHANFHPMDTCB7XGHAQ/explore/uttera[…]w=data&dataTabId=data-bcb74a67-07f2-4ad4-8b92-6169c6ffc169

---
Hoping this will give them a good idea on what they want to test themselves and also if they can get a blindset annotated with a ground truth they expect, we can support with more testing. (edited)

Nice job.  Trying to continue on - gone through the one class prompt which looks the best.
Made some light suggested updates just tightening the logic slightly - whether this was necessary/effective an interesting question!
Did an example with a key pair value rather than JSON - I think this reads much more easily in the tool to present.


[21:13] Mishra, Urvashi
Action items from today's call:

1. Create 2 workspaces for explicit/inferred and verbatim, and work on categories, sub-categories [Nipuna]
2. Load 1657 records into dataset in HumanFirst [Riddhi]
3. Load FAQs from Sonnet website into HumanFirst for Gap analysis [Riddhi]
4. Share Test data for FAQ [Riddhi]
 like 2
 [21:15] Broadhurst, Stephen
Nice, TQ.  My notes, couple of other things on there.

Data load

Conversations > 1000 utterances have protection against load.

1 convo exceeding with lots of duplicates.

Riddhi: pulling out that example and emailing so we can jointly review

Exclude that ID in the query at the moment to load for FAQ to proceed.

~1700 will get loaded then

FAQ report - splitting to two.

Two workspaces/grouping models same taxonomy.

1 Explicit - really really verbatim - with warning will have  things like "hhmm is that really the regulation" (even if this goes to out of scope/other)

2 Inferred - will be formatted in tone of FAQ - better format, wider variety, less tightly evidenced - more investigative

Can merge models if necessary - but likely to be quite different ground truths.

Confirmed can't (even with VDI) access the confluence pages.

Riddhi: sending CSV of the testing data for FAQ which includes FAQ categories and LLM expected example verbatims.

Stephen/Nipuna: Do the split of prompts for FAQ, do initial model build from the ~1700

In parallel Deloitte team working on Topics so we can progress both



For the topic model "col B" had ~60 topics in a three layer taxonomy - this is the framework to start with and do discovery.

Other "col C" had ~400 categories below that - unlevelled.  Agreed not harden this now with the client instead will use the 60 and cover the rest in discovery in tool

Deloitte team working on getting the topic prompts run on ~1700 



FAQ Sonnet website

Urvashi: Arranging for client to send or downloading and creating data set for gap analysis

Writer access done.


Stephen  [11:32 AM]
Riddhi loaded the data.
[01:51] Dasani, Riddhi
Hi Broadhurst, Stephen

Sorry for late message - coming back to desk for a quick message. 

For Data Load 
Conversations > 1000 utterances was not an issue - Still added a Clause in SQL Query to remove if this will ever be the case
Quick follow up on this : Does it mean Conversations > 1000 utterances is the limit just when we try loading it from Studio or same rule applied from API as well. 
I would imagine if really a long call happen - will we be discarding it from the ingestion itself if so all good but will make a note for client.

Actual Reason why that was happening is there were duplicates in Call Metadata table that was getting multiplied on Left Join
Added both these conditions in SQL query and it was successful data ingestion and hence latest details are as below 

Data Name: BQ_batch_July9_6_43
Total Number of Calls : 1658
Total Number of Utterances : 56907

Note : This batch has maximum number of utterance per conversation count to be 352 so we are way under our load limit but just wanted to highlight and while we are here thought will get the histogram as well of No of Utterances vs Frequency.

Next Step: I will send test data over tomorrow morning , just need to make transfers from Confluence to Excel and then run the queries too as Test team provided just conversation_id but I will do that first thing in the morning
 like 1
Screenshot 2024-07-09 at 8.46.05 PM.pngNipuna  [8:43 PM]
@mathieu Riddhi (Deloitte) is mentioning that she cannot use the API using the API service account you set up. I see it has write permissions access on the org level so all looks good. I think its either the .env file not loading correctly or they have the wrong user/pass.

I've asked her to verify that the username is the same as api@definity.serviceaccount.humanfirst.ai and try direct authentication instead of .env loads like so but waiting on a reply.
hf_api = humanfirst.apis.HFAPI(username=username,password=password)


Nipuna  [11:27 PM]
Quick update on the FAQ model build. I pulled out Explicit Verbatim questions with a prompt ran on all the conversations and split into two separate workspaces.
Explicit_Verbatim_FAQ_NBS -- 3,219 questions
Explicit_Verbatim_FAQ_Sonnet -- 1,313 questions

Started a bit on the Sonnet since we have a broad taxonomy from the Sonnet FAQ website. I think we might need more Sonnet data as most of 1,313 questions are conversational phrases lacking any context. The Other_Inquiries class will likely be pretty big. Will start on the NBS model tomorrow as well based on the taxonomy labelled for NBS on Riddi's CSV file below:

NBS:
['Billing', 'Renewal & Cancellation', 'Documents & Communication', 'Policy & Coverages', 'Underwriting Guidelines', 'Broker Technical Support', 'Policy & Coverage', 'Quoting'](edited)


So sonnet explicit https://studio.humanfirst.ai/playbooks/playbook-S2B6BXQWFNCJBLXXPLV52UKT/explore/uttera[…]CH&dataSortBy=uncertainty&dataSortDir=desc&groupBy=cluster
Model looks full of sensible things.
Has indeed lots of things that are just like the user said them like And now, the $385.50, I can make through my bank? but that goes into payments OK
Coverage is 45@0.7 and 80@0.35
Could keep going on uncertain clusters but getting things like
"So what would this be in the form of a letter or how does this going to be?"

Which is the prompt that created this 1,313 dataset?  I'm thinking we need to be careful of our version control of these.

Sonnet FAQs
https://www.sonnet.ca/faqs

So the explicit verbatims here are going to match to high level topics like Payments fine (SS1)
but the FAQs to the Sonnet actual FAQ information (SS2)
"is that going to make my payments change at all?"
"So there's no way I can just fast track that payment, like pay today type deal?"

In fact I'd query whether this is explicit data is very useful at all.

I'm not finding conversations from the test data in here

67e48f56-a1eb-5f99-97a9-89ffe222e5d4

@Nipuna my suggestion would be to move onto the Inferred prompt and get that run and a model starting to be created on that for sonnet, it's likely to be much more useful and more likely to reveal the long tail of answers for the gap analysis against the FAQs.


Suggested topics for call with Deloitte tonight
I can only make first 30minutes as have to join Ebay to run demo.


What is the Eta for FAQ extract of Sonnet and NBS webpage content?
We need to get more data in, x10 at least, with different convosation sets suggested for NBS and Sonnet.
Some ids in the test data aren't found in the loaded data is that intentional?
Test data format format needs stricter tabular format to allow automatic processing - to run CI/CD tests - one expected result per line, "no Or"
Need to store and version the data somewhere, confluence not a good choice, is there a git repo - similar for prompts and versioning outputs?
Test data is forcing the FAQs to the existing FAQs on the website is that the aim?  Is that not obscuring the granualarity actually necessary to answer these?
Explicit results are as requested, but as expected - extracting the user verbatim.  They have a lot of call/situation specific things and then match in very loose high level areas to FAQ pages - might be fine for a dashboard, but not really any god for gap analysis.
Inferred results seem much better for gap analysis and understnading the missing FAQs to increase deflection.
Nipuna  [3:27 PM]
Thank you for the deep dive and suggestions. I agree on the usefulness of the explicit data is questionable but if the high level categories match I think that's what their looking for.

I will get started on the Inferred prompt for Sonnet as I think that's the only way to do accurate gap detection as you mentioned. Also yes most of the test data is missing in the recently uploaded dataset.

Which is the prompt that created this 1,313 dataset? I'm thinking we need to be careful of our version control of these.The prompt that extracted this initial dataset I tried on the test data and got about 80% matching results for the 5-6 examples labelled Verbatim. There was a case where the test data contains questions from Agents in the Verbatim class which I will raise. I will save a log of the prompt used corresponding to the dataset generated for version control.
Stephen  [4:30 PM]
Great stuff, thanks Nipuna - anything you want to add to my topic list for call (or have me change) if not I think I'm going to put that in the chat there so that we can try and do some async and let you do more show and tell as needed in the call.
Nipuna  [4:31 PM]
No looks good to me, nothing else on my end.
Nipuna  [7:23 PM]
Sonnet Inferred model is much cleaner as expected. Got it to around 82@0.7 coverage/confidence with the same high level classes.
https://studio.humanfirst.ai/playbooks/playbook-YPAFLIKSEBEOFPO2B3Y3QOKE/explore/uttera[…]amespace=definity&intentId=intent-O2ECNCOF4VFGZLAEDKQBRCKS
Stephen  [5:08 PM]
Seeing a lot of ask to be up in front of the client - I make this 12 meetings a week (5 Deloitte/Definity standups, 5 Deloitte standups, 2 joint working sessions existing) (edited) 
image.png [5:09 PM]Seems like whilst I was on the call on Thursday, certain things agreed, then after I've left Deloitte tried to bend it back again reagreeing the opposite.
[5:12 PM]@dubois concerned that Deloitte increasingly treating Nipuna as a FT resource to directly manage.
Nipuna  [5:16 PM]
Yea I mentioned to Urvashi a few times that I'd stick mostly to the 2 weekly touch points unless major blocks happen. It's never going to be possible to join their daily stand ups.
dubois  [5:17 PM]
Why don’t we create our own standup that we control and we invite deloitte and definity?
dubois  [5:18 PM]
And let them do their many standups without us
Nipuna  [8:42 PM]
@Stephen been chipping away at the Sonnet Explicit model.

Updates

Used 5000 out of 10k new calls from dataset to generate around (~3.8k new verbatim questions and 10k NBS verbatim questions).
For now setup the classes as they wanted (Auto, Home, Other) under 3 of the parents. Rest are all a single parent class with no children, exactly matching their FAQ page.
For some classes its hard to find training data from Verbatim's

Sitting at ~77% F1 and 66%@0.7 coverage
Still some disambig to do as verbatim questions are very varied in phrasing.



Also, imported the existing FAQ model into separate workspace for doing Gap Analysis from Riddhi's CSV (workspace name: Existing_Sonnet_FAQ_Model)

Think as you mentioned we're going to have to rely on Inferred to get accurate coverage metrics.


Still need to start on the NBS model -- waiting for Riddhi to provide a description of taxonomy since no examples to go off like Sonnet. Deloitte wants to combine NBS and Sonnet together into one model which should be possible but mentioned will build separate and merge later. (edited) 
Stephen  [9:38 PM]
Apologies that your verbatim work gone to waste - but as you saw in call probably for the best!

I feel like we're getting to the point where we have enough data, and are clearing the problems to make progress.  Call pragmatic and making the right decisions after they've been batted around across the Deloitte leadership and then the client.  So have every confidence in you being able to do a great job whilst I'm away.

Here's some background on what is going on behind the scenes:

PM (Urvashi/Sam) is being trapped by her client/leadership into holding dates, whilst they are delaying making decisions, ignoring sound advice, and not acknowledging reversal of decisions, wasted effort and resultant scope changes.
This is common with junior PMs and an unclear scope - Deloitte have failed to be strongly managing enough their project early on delaying start and inputs but not managing the end date or resource profile, and then pushing the resultant issues down onto the team or subcontractors.
Please don't feel you are pushed into committing to things being done on a certain date  you are uncomfortable with.
Always feel free to say "I'll go and look at it but can't commit here."  "We'll help as much as can towards your goals etc." - if you feel it's going to be a sticky meeting on deadlines, pull @dubois in.
Similarly with meetings - arbitary meetings help no-one - the meetings we have at the moment have progress and momemtum - that's great we should double down and just get on with what we need.
Creating double daily check-ins is normally a reaction to their project being under-review (internally by Deloitte risk) and needing to show some "extra oversighte" - it's a bad reaction to the problem and helps no-one.
Inviting the client to an internal meeting at no notice is also very bad form.
As background we don't have a contractual date, acceptance criteria scope etc
We're just doing everything we can to get the client the best reports possible and make Deloitte look good - I feel we're going to do a great job on that.
My guidance would be to just stick close to Olivier and Riddhi - they really want to make things work and are doing good things.
Olivier was spot on - I'm leaving the meeting now to do some work!

Minutes I posted with those decisions in their Slack - I would be careful to document like that any decisions that are key to scope.
Being clear on what will or won't be done helps everyone.

2024-07-15
* standups - focusing on Tue/Thu meetings - happy to step into any specific issue meetings - can't attend routinely others.
* Dropping verbatims, swapping to inferred as much better data fit with Website FAQs provided.
* Had been working on that report, will now refocus on inferred.
* sub categories for FAQ reports - dropping Auto/Other/Home - going with discovered categories.
* data volumes - at 10k, getting to 30k rapidly 20/10 past threshold
* VDI - a pain but pushing on.
* Website FAQs received and loaded.
* Gemini speed - Think that 1.5 needed for transcript size - Olivier going to raise how to raise Token limits - 300 at moment, going to make the large set slow unless that can be done
* Wednesday touch in to be arranged tomorrow.
* Deloitte leadership meeting Thrusday - will aim to have as much done as posssible but can't make a commit on the call given changesNipuna  [10:00 PM]
Understood thank you for the deep dive and the advice. I agree Urvashi is a all over the place, but Riddhi and Olivier are much more realistic and oriented. It's strange since the team doubled down on Verbatim last week and proposed that was only what client wanted and have now completely switched even though we've been saying that for 3 calls.
[10:00 PM]Regardless for tomorrow, will need to sync with you on how to best use the coverage data for showing the gaps. (edited) 
Nipuna  [10:27 PM]
Had a quick chat with Riddhi on FAQ Gap Analysis. Everyone else was out.

Followed the standard process: Generated 5-10 questions from the answer units. Added as labelled data under each FAQ question as a class. Sort by uncertainty shows the lowest covered. Currently available in this workspace.
Riddhi seemed to pleased with the process and said made sense. Asked questions around the confidence clip and we looked at uncertainty between 30-70 to see the middle ground to determine when a question is considered existing  vs new . 
She mentioned that Sonnet FAQ page is meant to remain static most of the time, and if any updates were made the client would need to also come and update the gap model via the steps taken - I confirmed yes.
Confirmed gap analysis is only for Sonnet.


Tomorrows Meeting

Meeting with Samantha, Miguel, and Anand - Senior Managers Deloitte
Overall they want to see progress on FAQ report. Made it clear to Riddhi that due to the last minute change, this was the current state of what we got up to and she mentioned that was fine. Overall idea is to show conversations --> inferred questions (prompt, workspace) --> categories/taxonomy --> gap analysis.
Also made it clear that due to no taxonomy description provided for NBS, Sonnet was being prio'd. She confirmed person responsible on Definity side is out for PTO until 29th so not going to get much there and to continue focus on Sonnet for short-term.



Nipuna
  Jul 17th, 2024 at 10:41 PM
@Stephen a follow up questions I had:
Can we keep the gap analysis as an entirely separate process from the taxonomy model (provides Main Category / Sub Category)?
Since gap analysis just needs to tag a question with existing, new the confidence score is the only determining factor.
The taxonomy model would be a separate batchPredict call and provide a Main Category / Sub Category without need to go into extreme granularity with Sub Categories
Main reason I am asking is then we don't need to match the granularity of the Gap Analysis model (each question is a class) to the Inferred FAQ Taxonomy Model and can just have some simple Sub Categories?
image.png
 
image.png



Stephen
  Jul 18th, 2024 at 6:40 AM
Probably should align the two models.  Could do that with three levels to square the circle
RHS
High Level, Medium
LHS
HIgh Level, Medium, FAQ level

Nipuna  [9:40 PM]
@mathieu Not Super Urgent but have QQ since Stephen's out & I need some help for Definity.

So currently we've built a NLU model from FAQs extracted using a prompt and Gemini. The conversations were so far entirely English based and outputs were English questions extracted. Now, they're planning on bringing in French Conversations dataset. Given that the prompt extracts FAQ questions in English regardless of it being fed a French convo, as far as I know we don't need to do anything additional.

However, if we were required to also have a separate French question extraction prompt, would that work with the same NLU model built around english questions extracted?

My understanding is since its USE, its language agnostic but would we have a case where we need to also label french questions data into the training? This is assuming the context/concepts being talked about in English vs. French calls is all the same stuff, difference is language being spoken.
7 repliesmathieu  [9:42 PM]
the cross-lingual performance of USE is pretty good. we were testing english training sets with french test phrases with great results
[9:44 PM]LLMs will also easily give you english topics for french conversations
[9:44 PM]I haven’t validated how accurate these are though
Nipuna  [9:45 PM]
ok perfect! And to test this incase we need to prove would the scenario below work:


setup two separate blindests of exact same French/English questions 
run two evaluations with each test set 
results should be fairly close to each other 
mathieu  [9:46 PM]
You should be able to add “Answer in French” to the prompt without changing the prompt’s contents I think. That test scenario seems good.
[9:47 PM]by virtue of the way token embeddings are managed inside USE, mixing languages together (as we do in Quebec) also works very well

you can start a question in english puis la finir en francais
Nipuna  [9:48 PM]
Ahh ok great! Thanks for the clarification :raised_hands:


Nipuna  [10:27 PM]
QQ for an ask from Deloitte. They've sold this dashboard view to Definity and want to group by a frequency of similar FAQ questions extracted. They're now realizing that need to do semantic similarity since not all questions are going to be extracted the same if they want an accurate frequency grouping, instead of just a total count.

Is there any way we can support in this /  they can use us for that? The extracted questions would technically exist as embeddings in HF but the clustering also needs to be dynamically updated based on the filtering (date, category) which is even harder lol. From my understanding this isn't possible at all unless they setup a separate vector db.

Easiest replacement is make frequency a count on the sub categories to at least highlight the categorical frequency. (edited) 
image.png 6 repliesNipuna  [8:46 PM]
@mathieu can I get your quick input on this when you have a chance ^
Stephen  [8:21 PM]
Earth in the project we covered that they would need to have a classification model for this  with a clip and then there would be an “other” pile (below clip) that would need regular (say weekly or monthly) review in humanfirst to breakdown the new topics  (edited) 
[8:23 PM]@Nipuna this should provide for everything in the chart (just with an other class) is this not enough for what they need?
mathieu  [8:25 PM]
that’s a hard one... vector dbs won’t do any clustering (unless someone added that feature recently)

we can cluster things through the API but clustering always looks at a subsample of data (it’s O(n^2), it’s too slow to do in real-time over everyting). This means that their estimate of “frequency” would have to create a label from a cluster, then train an NLU model and extract coverage information.

^appologies this was stuck in my drafts for some reason :facepalm:
Nipuna  [8:38 PM]
Ty for the reply Matt! Yeah I figured this would be hard to do in realtime and conveyed that to them.

I believe they have communicated with Definity on this and have decided to just make it a Frequency Total Count on the Sub Category. I've tried my best to keep a good amount of granularity in the Sub Cat to support that.

@Stephen Its less of a problem of identifying new topics but more how they are ordering the similar questions in the Tableau dashboard view. Since similar extracted questions asking the same thing aren't phrased exactly the same, they were looking for a way to do frequency by Clustering like how we do in the tool which is out of scope.
Stephen  [1:07 PM]
So I think active clustering is a separate topic - and one that keeps bubbling up.

But this is what the classification model was for and the need to do it down to ~ an FAQ title level.  It groups unique outputs by semantic similarity to a taxonomy and lets you have the frequency in these charts.  Then you have a bucket of other beneath clip and you then explore that to iteratively expand your model and FAQ coverage. (edited)


Nipuna  [5:14 PM]
Just posting some initial test results from the Semantic Similarity. I haven't reviewed this in depth but sharing to get your input as well @Stephen. This is purely for CALL data from NBS/Sonnet for English/French (only excluding Chat data).

Test Team Questions: 89 Questions Extracted for 49 Unique Conversation Ids
Prompt Questions Extracted: 129 Questions for 40 Unique Conversation Ids (from that test set a few were missing in the tool)

Out of those 129 questions extracted, each prompt FAQ was compared via semantic similarity to every single test team FAQ related to the conversation ID. Then a confidence clip of 0.55 was used to mark whether its a pass/fail. 0.55 was chosen as from a quick glance, the prompt FAQs had much more detail than the Test Team FAQs and this seemed like a good place to start.

From the 129 prompt FAQs @ 0.55 confidence clip, 65 passed and 64 failed. From what I see, a fail would also include a scenario where the prompt extracted net new FAQs that the test team didn't identify. Therefore those new questions are also getting marked as fail.

Below are two files:

extracted-q-semantic-sim-test -- which contains purely the prompt extracted  FAQs and their corresponding batchResults and finally the semantic similarity test results. 
sem_sim_match_question - highest matching semantically similar question from test set
sem_sim_score - contains the score of the highest matching question
result - pass/fail based on confidence clip of 0.55
test_team_arr - all the questions identified by test team for that convoID
sem_sim_matches - total match array with all scores

mapped_to_ground_truth -- is a left join of the test results onto ground truth based on convoID and test team FAQ matching the top match semantic similar question


I guess next steps are to review the failure cases and then identify how many of those are net new questions and how many are actual failures where the prompt didn't identify the test team questions.

I'm going to shift gears to finish off the chat data prompt as promised to Deloitte for rest of today but thats where the testing is at.
2 files extracted-q-semantic-sim-test.xlsxExcel Spreadsheetmapped_to_ground_truth.xlsxExcel SpreadsheetNipuna  [9:54 PM]
Senior Agent Report Debrief

Use Case

Tableau output seems to be mostly statistical calculations and trends reporting
HF involvement side comes down to reasons area highlighted in area of screenshot (first box)
Urvashi didn't still have a clear understanding of what "Reason" would represent whether it be phrases or categories in the dashboard this morning. 
Suggested definitely doing 4-10 clear categories for NBS/Sonnet escalations separated.


Data

Currently two types of calls in Sonnet/NBS
Data load is ongoing but low, especially for Sonnet
~900 calls for NBS 
~280 calls for Sonnet
Only 28 "support" calls from junior to senior that are actually where an escalation reason may be present
Remainder ~250 are outbound calls from senior agent to customer where escalation reason is unlikely to be mentioned


I'm working on prompt to identify categories for Sonnet / Riddhi on NBS
Made  clear only thing I can do with this low amount is to verify whether 250 will provide reasons or not until more data is loaded

Riddhi blocked on finding more "support" calls until business provides better logic. They are trying to solve with business actively.


Next Steps

Same process that followed for Topic Model reasons: Prompt output of clear escalation categories --> Simple 10-12 intent topic model
I asked Riddhi to get business to provide some categories so test data and prompt predictions are aligned
She got back with 3 classes since this morning which is atleast a starting point (more to discover once I have more than 28 calls)
Front Line Agent Errors ( Wrong info provided ) = Knowledge Gap 
Stubborn Customer 
Website / Communication Unclear


Will get started on prompt
(edited)
[9:58 PM]Screenshot 2024-08-13 at 10.46.02 AM.png dubois  [10:21 PM]
@Stephen @Nipuna Anand and Samantha have agreed to quick standups every 2nd day with us to mitigate miscommunication between HF and Deloitte and what we’re delivering.
Stephen  [10:25 PM]
Every second day = 2 or 3 times a week?
dubois  [10:27 PM]
Id do 2x per week for 20 min
Stephen  [10:29 PM]
That sounds positive and manageable - I think Nipuna’s summary is very clear.  The project is up against it we are there helping but we have to get data in and a definition of what we need to do then we can start clearing the blockers and the tasks away or it as fast as possible.


Nipuna  [5:14 PM]
Just posting some initial test results from the Semantic Similarity. I haven't reviewed this in depth but sharing to get your input as well @Stephen. This is purely for CALL data from NBS/Sonnet for English/French (only excluding Chat data).

Test Team Questions: 89 Questions Extracted for 49 Unique Conversation Ids
Prompt Questions Extracted: 129 Questions for 40 Unique Conversation Ids (from that test set a few were missing in the tool)

Out of those 129 questions extracted, each prompt FAQ was compared via semantic similarity to every single test team FAQ related to the conversation ID. Then a confidence clip of 0.55 was used to mark whether its a pass/fail. 0.55 was chosen as from a quick glance, the prompt FAQs had much more detail than the Test Team FAQs and this seemed like a good place to start.

From the 129 prompt FAQs @ 0.55 confidence clip, 65 passed and 64 failed. From what I see, a fail would also include a scenario where the prompt extracted net new FAQs that the test team didn't identify. Therefore those new questions are also getting marked as fail.

Below are two files:

extracted-q-semantic-sim-test -- which contains purely the prompt extracted  FAQs and their corresponding batchResults and finally the semantic similarity test results. 
sem_sim_match_question - highest matching semantically similar question from test set
sem_sim_score - contains the score of the highest matching question
result - pass/fail based on confidence clip of 0.55
test_team_arr - all the questions identified by test team for that convoID
sem_sim_matches - total match array with all scores

mapped_to_ground_truth -- is a left join of the test results onto ground truth based on convoID and test team FAQ matching the top match semantic similar question


I guess next steps are to review the failure cases and then identify how many of those are net new questions and how many are actual failures where the prompt didn't identify the test team questions.

I'm going to shift gears to finish off the chat data prompt as promised to Deloitte for rest of today but thats where the testing is at.
2 files extracted-q-semantic-sim-test.xlsxExcel Spreadsheetmapped_to_ground_truth.xlsxExcel SpreadsheetNipuna  [9:54 PM]
Senior Agent Report Debrief

Use Case

Tableau output seems to be mostly statistical calculations and trends reporting
HF involvement side comes down to reasons area highlighted in area of screenshot (first box)
Urvashi didn't still have a clear understanding of what "Reason" would represent whether it be phrases or categories in the dashboard this morning. 
Suggested definitely doing 4-10 clear categories for NBS/Sonnet escalations separated.


Data

Currently two types of calls in Sonnet/NBS
Data load is ongoing but low, especially for Sonnet
~900 calls for NBS 
~280 calls for Sonnet
Only 28 "support" calls from junior to senior that are actually where an escalation reason may be present
Remainder ~250 are outbound calls from senior agent to customer where escalation reason is unlikely to be mentioned


I'm working on prompt to identify categories for Sonnet / Riddhi on NBS
Made  clear only thing I can do with this low amount is to verify whether 250 will provide reasons or not until more data is loaded

Riddhi blocked on finding more "support" calls until business provides better logic. They are trying to solve with business actively.


Next Steps

Same process that followed for Topic Model reasons: Prompt output of clear escalation categories --> Simple 10-12 intent topic model
I asked Riddhi to get business to provide some categories so test data and prompt predictions are aligned
She got back with 3 classes since this morning which is atleast a starting point (more to discover once I have more than 28 calls)
Front Line Agent Errors ( Wrong info provided ) = Knowledge Gap 
Stubborn Customer 
Website / Communication Unclear


Will get started on prompt
(edited)
[9:58 PM]Screenshot 2024-08-13 at 10.46.02 AM.png dubois  [10:21 PM]
@Stephen @Nipuna Anand and Samantha have agreed to quick standups every 2nd day with us to mitigate miscommunication between HF and Deloitte and what we’re delivering.
Stephen  [10:25 PM]
Every second day = 2 or 3 times a week?
dubois  [10:27 PM]
Id do 2x per week for 20 min
Stephen  [10:29 PM]
That sounds positive and manageable - I think Nipuna’s summary is very clear.  The project is up against it we are there helping but we have to get data in and a definition of what we need to do then we can start clearing the blockers and the tasks away or it as fast as possible.


Nipuna  [10:45 PM]
Finally closed out the sem similarity testing. Ran through the FAQ test team data for both Calls/Chat

The two CSVs attached have all the ground truth's annotated with a pass/fail, matching prompt extracted FAQ, similarity score and other useful fields. Also added a seperate tab with all the extracted FAQs from the prompt with the ones that matched marked, so net new questions can be identified.
Chat results seem much better perhaps b/c chat msgs are more direct / its running on Anthropic instead of Gemini 


Current Semantic Similarity Test Results for FAQ Report:

Calls 
Total Valid Questions Tested: 82
Total Pass: 49
Total Fail: 33
Pass Rate: 60% @ confidence clip 0.55

Chat
Total Valid Questions Tested: 46
Total Pass: 38
Total Fail: 8
Pass Rate: 82% @ confidence clip 0.55


Notebook also attached. It produces two CSVs
Appended ground truth csv: Left join onto ground truth with matching prompt FAQ / predictions / sem similarity
Net prompt extracted questions and predictions: questions that matched are marked with "matched" to make it easy to identify net new questions

(edited)
3 files Chat_Final_Semantic_Sim_Results.xlsxExcel SpreadsheetCalls_Final_Semantic_Sim_Results.xlsxExcel Spreadsheetfixed_sem_sim_faqs.ipynbBinaryNipuna  [9:03 PM]
Did some more work on the Sonnet Senior Agent Escalation Prompt to output useful escalation reason categories to a reasonable granularity.

Tried to define a few more categories than general reason category to make it more useful
Tried to get Other class to have a highlevel parent "Frontline Agent Error with Other" so better than just "Other". Definity Analytics team can drop down into the tool and filter to find reasons to add to prompt.


I am thinking keeping two separate prompts is needed to get best results for Sonnet as context is different:

Escalation Calls: Senior Agent Outbound Dialling Customers Directly. ~70% of calls here have no escalation reason mentioned and end up in "None" so only ~30% have useful information. It should be noted though that categories here are quite inferred given the context. Categories could be reduced here if needed.
Support Calls: Junior Agent Inbound Dialling Senior Agent. Only 28 calls but good distribution of reasons.


The biggest categories in each are highlighted. (edited) 
4 files image.pngPNGimage.pngPNGEscalationCallPrompt-V2.txtPlain TextSupportCallPrompt-V4.txtPlain TextStephen  [1:38 PM]
OK - starting with dropping my work in a similar format here then we can correlate

Prompt updated after reviewing the sheet attached across Sonnet and NBS

Category	                         Ttl   %
Agent Reassurance or Confidence	      51   5%
Customer Service Complaint	          10   1%
Documentation or Process Unclear	 266  28%
Frontline Agent Error	              41   4%
Other	                               3   0%
Product or Discount Eligibility	      31   3%
Reverse Accidentally Made Change 	   5   1%
Stubborn Customer	                   9   1%
System Error	                      92  10%
Underwriting Clarification	         438  46%
Grand Total	                         946 100%https://studio.humanfirst.ai/playbooks/playbook-GD7D67OB45CL7PNOYJTHTW4W/explore/uttera[…]A%3Areason%3A%3Afalse&showDuplicates=true&showLabeled=true
This has low variability between runs at 1.6-1.7% at 0.1 temperature - confusion matrices in sheet (edited) 
2 files 2024_08_20 Sra Prompt After Inspiration.txtPlain TextSRA NBS Confusion Matrices.xlsxExcel SpreadsheetStephen  [1:46 PM]
Things to talk through pre Deloitte call then on Deloitte call


Is it helpful to split Escalation and Support Call prompts - do Deloitte have two different reports for these data sets to fit in?
Is the increased number of the groups helpful?  24 and 14 respectively Sonnet, > 10 NBS - how does it fit into the report.  Does the number of categories with them more detailed format in Sonnet snowball when hitting real production data.
Does the expectation in one Sonnet set expectation in the other NBS?
Are the sonnet more finely granulated groups supported by the data - i.e with such small samples it is very likely not all groups are found - so by giving the prompt a clear list of groups that are valid,  if it's a new Knowledge Gap in production not in the test set - for instance "Knowledge Gap with how to unlock computer." - How is the system going to react to that - are we being too prescriptive?
Prompts seem complicated with a lot of groups - how stable run to run are these across runs - I found high variability with Claude until I simplified my prompt.
Does the Sonnet prompt set an expectation of increased complexity in the NBS prompt?
The Sonnet prompt seems much harder to digest?
Do we need snippets, or just reasoning?
Nipuna  [7:25 PM]
Hi Stephen, Nipuna,

Can you please provide the HumanFirst IPs for Production, so that Sreekar (CC’d here), can get it whitelisted, and then get required approvals from Security team? We need this information as soon as possible.
Sreekar is part of Definity’s DevOps team.

Thanks in advance!

Regards,
Urvashi@mathieu I'm going to loop you into this email thread
Stephen  [8:51 PM]
Short list
Intents
+ None - with defaulting to none.
+ Customer Error
Intents from Topic cover subcats.
Consolidating prompt without the rules
27 we are at 578
272 we are at 285
Are we going to split two reports?



Stephen  [2:10 PM]
FAQ: Gemini - training data was already in that
Topic: Claude (intent/reason)
Sra: Claude
Callback TBDNipuna  [10:22 PM]
Didn't have too much time today but after some testing, I think we're going to have to go with two separate prompts between Sonnet Escalation and Sonnet Support calls. With a single prompt, despite describing the two different context, the prompt seems to get confused and assign None much more frequently.

Its reasoning gets confused trying to balance both the context that it may be a Customer (Escalation) calls or it may be an Junior Agent (Support): "The conversation appears to be a direct interaction between a senior agent and a customer, with no indication of a frontline agent escalation or involvement." 
Quite a few calls from the test set that should have reasons are getting marked as None especially in the Escalation calls segment. This is mainly because the prompt is trying to identify a clear escalation reason for the escalation calls where as it sort of actually needs to be allowed to infer more // different from Support calls where reasons should be clearly available.
Combo Prompt V2 I tried to describe the buckets to help it but it actually tightened further and put more in None.
All three prompts (NBS calls, Sonnet Support, Sonnet Escalations) all share the same taxonomy so they are aligned. Just three different prompts.


So keeping Escalation/Support as individual prompts is best rather than mix two different context together. Also, need to get the testing team set CSV from Deloitte without confidential blocker so we can actually check how the outputs compare. (edited)


Stephen  [2:29 PM]
Stephen Broadhurst
1:28 PM (0 minutes ago)



to Alex, Urvashi, nipuna@humanfirst.ai, Nipuna, Stephen, Riddhi, Samantha





Here is the marked up version for internal discussion first.
Normally these questions come from pretty specific people, this looks like the Advanced Analytics team do you know who drafted this questions for this one?  
It may be that responding to this is greatly helped by setting up some time with them to get them trained on the processes they are asking about.
What would be the people that need to be involved with that?

I've tried to give a concise draft answer to each on the sheet as people normally like a comprehensive response as well as any sessions around.  

As a high level summary, these are the things that we can do as HF directly to address the things raised in the doc. 

HF Suggested Actions
Do a walkthrough of workspace migration processes and options in HF with the Definity team that needs to maintain the solution.
Do a deep dive to answer any technical or "under-the-hood" questions on the HF pipelines and models in use
Help rename all the workspaces to the requested standard
Setup Definity continuing touch ins and any specific training sessions they want as part of their support package

Then below are the things I suggest we should talk through as a project today. We can give advice and tool or api options or examples for how the project best addresses then, but the decisions on the questions will have delivery impacts that will generate work for the Deloitte and Definity team.

Project Discussion Points
How are configuration IDs maintained in the end to end system on upgrade - two options
1) by easy to change configuration of the DAGs etc and automated report into confluence - this is easy for the client - create the new workspace however like, change the id, everything is up to date.
2) trying to keep the ids fixed during migration - this will need a much more rigorous delivery process, as the id before has to be the id after. 

Where is the E2E configuration of the environment documented in Confluence - is this of sufficient detail for the Definity team to understand as there are a lot of end to end components and requests for documentation here? Is it worth making some of this auto generated from configuration?

Where or is there a log of produced output from HF kept in Big Query - this may be a project scope gap if it is expected?

We've been helping with example code snippets and code examples through the project, the expectation was that this was going to be rewritten into whatever required format required for the end to end integration and go into a code review and PR process for anything that would become a deliverable. The document raises questions about notebooks in Bitbucket which is something we don't have access to. What's the intended PR and code review process for any notebooks that are forming part of the final Deloitte deliverable?

Definity have a quantitative versus qualitative model selection question - Claude v Sonnet - again this doesn't seem in scope but is a possible further work item. We should talk through how that decision was arrived at, any quantitative requirements for it and what response is best here.
https://docs.google.com/spreadsheets/d/1-S7uV-_lB53Yft2lVhMw3aUYWkKXjQlH/edit?usp=sharing&ouid=103791632676830510243&rtpof=true&sd=trueExcel Spreadsheet Questions from AA team for HumanFirst - 2024-08-21 SB Notes.xlsxGoogle Excel SpreadsheetNipuna  [11:20 PM]
Got a new prompt that mapped Underwriting Clarification to Policy Clarification. Redid the annotation for most of Sonnet. Results seem valid but a few more calls to check.

NBS seems much more complicated to match with ground truth as the reasons are much longer. Still did a left join on the ground truth data and annotated prompt results. I attached the file here, will pickup on Monday. (edited) 
Excel Spreadsheet RebaselineNewPrompt.xlsxExcel SpreadsheetNipuna  [11:49 PM]
replied to a thread:Ok understood, going to have to do the NBS rebaseline tomorrow as got caught up with Verizon and finishing up a deck for Deloitte today. There's 35 convos in the NBS dataset so it will take some time to review.

So far the Sonnet Support/Escalation is looking great. The fails are quite ambiguous cases where it could match the test team category or the prompt category equally but left as Fail.

Link to the deck with a few examples, distributions over the dataset.
https://docs.google.com/presentation/d/1vYqZvPxiZrW-wnH181qnbiNRgTPp_zLnEKjPLGzeBaA/edit?usp=sharing
4 files image.pngPNGimage.pngPNGimage.pngPNGDeloitte-SRA-Report-UpdateGoogle SlideStephen  [3:04 PM]
Only Sam on call @dubois she wants to talk contracts with you?
She didn't really know how the go live had gone - but though OK.
Neither QA status, or data availability for final report.
Didn't want to talk through anything else in any detail.
Urvashi expecting to be on 15:00 EST / 20:00 UKStephen  [10:32 PM]
Good news:  Had a very positive review on all the data, FAQ report live, Definity team very happy, all set for business review 29th.
Had one full prod data set for FAQ report run through.
Bad news: At the end Deloitte started to ask some quite naive/late questions again on approach having skipped object clearup to get there.  Turns out they've implemented their ETL in a very weird way.



What we expected - 1 convoset, multiple files. (is this correct - are there any bits that don't work/aren't implemented ourside forcing them the other way)
We were expecting one convoset per environment, files every hour, newest file with date, delete the oldest to maintain a certain data range.  Pipeline caching means it shouldn't rerun the old data unless prompt changes. Check the pipeline completion Then download just the data you want from the pipeline, limiting your query by the date range you are interested on.   In workspace you should see the rolling window of data and all the results to monitor or create new classes

What has been implemented - 1 convoset - per file unlink and link new to worksapce
So every (say hour) a new convoset is created a single file for the period put in, old is detatched from workspace, new is attached to workspace, pipeline is run on everything - no cache and the full data result from the pipeline is downloaded.  At the moment Deloitte not cleaning up the Convosets, but they planned to.
This means that you never see previous runs of pipeline in the tool.  Data is effectively lost - so Deloitte have to do the storage in BigQuery completedly.
It also means that there is a lot of confusing convosets, a lot of linking and unlinking going on etc.

@mathieu need to talk through this tomorrow if possible please?  I want to work out is what Deloitte done OK, if it's not OK and they have to rework it - does everything for the way we thought it should work work, as they will be very pissed if they have to do substantial rework and then it turns out not to actually do the bits.

I guess to try and get some async done


does the pipeline caching mean if a new file is added to a convoset and the pipeline rerun it only runs on the new file?  I.e token costs are not magnified by rerunning already run data.
how does the data appear in the runs button in HF - if I uploaded 16 files, deleted the oldest 1 have run the pipeline 16 times, should I be able to step back through all 16, what happens when I get to run 1 when the data deleted.
can I download from the pipeline via API just a limited set of data based on a data range - I feel that we should with created_date, but it will be original sourceConversation created_date.
mathieu  [12:14 AM]

pipeline caching is currently independent of conversationsets, and is kept on a per-pipeline basis so as long as you keep the same pipeline then you get caching
by default pipeline runs are not cumulative (to avoid the explosion of data) so you don’t see previous runs like when you use it with the stash
the created at date will be the one of the pipeline run unfortunately, filerting will likely be feasible once we have joins in place (in progress right now)


not asked but, why are they doing these silly things? are they just working out again a datapoint limit of some kind?
Stephen  [9:09 AM]
It's a junior team rushing after being forced into a difficult situation by their PM.
They've stitched together the project just in time for their GoLive however they could make it work, having not really taking the time to really do an end to end design.
So their first version that end to end works was linking and unlinking, and they've pushed that live, having truncated any proper test phase, and now looking in the tool working out the implications on that on what they see and how it works.
On our side everything is evolving fast and there isn't really a clear documented template for how the components/apis are supposed to sit together in this sort of advanced analytics project.  We've cleared the way point by point on APIs and blocks to let them get through the flow but everyone has been focused on the tactical, as Deloitte were system integrators and getting paid for all the end to end architecture, integration we haven't had visibility or time/money/bandwidth to stop them and force reviews and walkthroughs of deliverables.
I think we do need to sit down and work out how a user is supposed to see historic data for a pipeline over time, and how incremental syncs out to something like BQ are going to work.  I  know that this is in track, but Deloitte are having to try and build it on the fly in front of the customer.[9:13 AM]I think 3 has been the killer reason for why they've done it like this - they need to be able to upload a full hour of data, then download the results for just that hour and put it into BiqQuery and calculate their aggregations.   They can then track each hour is processed successfully and is available in the dashboards.

With no way to filter their query for the pipeline, if they are adding the files culmatively to a convoset, after each pipeline run, they'd get an increasingly enormous download of data, of which an increasingly small amount would be relevant.

So creating a new convoset each time and doing the linking and unlinking means they know that when the pipeline runs and is finished and donwloaded they've only paid to process the data they need in VertexAI (the culmative/caching question I think is a case of lack of understanding and confidence it definitely works like that), and then when they download it only has the relevant data they need (which does seem like a hard block with filtering as it is now)


1 file per convoset v many file per convoset
 TL:DR is we don't see a hard blocker with 1 file per convoset but it's not the expected design so features aren't optimised for it. Most necessary maintenance activities seem possible but they have different steps 

Sorry long post, detailed walkthrough of comparison. Can also walk through the evening and answer questions

Expected design is many files per convoset.
 * upload a new file for a period with a (typically ISODate containing) name representing it's duration
 * check the contents of the convoset for the total number of files/duration you want to maintain.
 * remove the oldest file if necessary 
 * when you upload that file you add it with whatever metadata you need to filter on later (for instance timestamp or batch run field)
 * pipeline runs and checks it's cache, as long as prompt has not changed, will only run on new information. 
 * if prompt was changed it would rerun on every file present and keep the view up to date.
 * pipeline copies source conversation metadata to pipeline output so output can be filtered by the batch upload id/timestamp range.
 * query the pipeline output with the metadata filter to download only the data relevant to the file you are interested in.

 + GUI is built to summarise the convoset as a folder containing many files so things like
 . easy at a glance to see what information streams you have on the data page
 . convoset folders summarise their total contents as data points make knowing how big each stream is currently easy.
 + no linking and unlinking, one workspace stays connected to one convoset
 + data is immediately available in the tool for examination for the full duration maintained in the convoset
 . individual runs won't show due to caching it'll all be contained in a single view on the latest run.
 + you can reprocess your convest data window automatically if your prompt design changes.
 - you can end up triggering a big rerun if you change your prompt or prompt settings depending on how much rolling data window you leave in your convoset.
 - pipeline results will potentially grow to be very large in tool - may want to clear the pipeline at points in the year 
 (Welcome feedback on what the process would be if you wanted to adopt this and what dedicated in tool controls migth be helpful)

Design as is is one file per convoset (summary of as understood implementatoin)
 * create a new convoset for a period with an ISODate name representing it's duration and environment.
 * upload a single file to it.
 * unlink any other convosets from the environment workspace
 * connect the new convoset 
 * delete any other unwanted convosets (to be completed)
 * run pipeline (there will be nothing cached as new convoset)
 * download entire pipeline output without filter.

- You must manually sum all the convosets for an environment to work out datapoints
. the (i) report contains some useful information to assist with this.
. Data Management page does have filter so can view only convosets for qa|dev|prod but it's less convenient
 - Workspaces must have convosets linked and unlinked as an automated and manual step
 + A pipeline can never run for more data than a single file as it's only ever pointed at one convoset.
 + No filtering on download is necessary
 . the latest set of data should be linked to the workspace ready for examination
 - previously convosets won't be
 . to view older data or reprocess - a clone environment can be taken and multiple convosets linked to a single clone workspace
 + no pipeline output data volume maintenance should be necessary it will only ever have the single run of data in for the convoset
has context menuStephen  [2:04 PM]
@John question re commercials for Definity - they have access to 1 namespace in the contract.
For a PS firm (i.e Deloitte) that makes sense to me Deloitte (versay) buy 1 namespace from us per client under their org, and then resell it to their client
For Definity though we're selling direct, they have a dedicated Org, and we had in sales two namespaces, Definity and Definity-Embeddings (because different embeddings each require a new namespace).
With a $200k direct contract typically a client would be able to have say 1 namespace for Dev/QA, and 1 namepsace for Production (often a PII requirement to segregate)
Or to have say one namespace for Sonnet and one for NBS their different internal business units.

Is there some reasoning in the Definity negotiation to limit them to a single workspace?

It's just making things hard to manage in the project  because they have to put every workspace for every report and every environment in one place
Stephen  [3:20 PM]
Sam/Anand/Alex no show - ran through with Urvashi for 10mins

Deloitte said they agreed with Sheryas FAQ, Topic no logging of metadata, SRA and Callback logging.
She was interested why it was so important for Shreyas as he wasn't letting it go - explained how it doesn't affect the actual result in Tableau it's pretty vital to debug what changed in case of prompt updates, and to be able to audit/report on - basically any acceptance/maintenance client criteria - I think she got the context then.  She hasn't been able to attend any of the Tuesday/Thursday meetings where this was discussed in detail, and with Shreyas so catching herself up.
There was a late change to standardise the output field names NBS to Sonnet, everyone just running through the update and the update of decks.
Ran through high level the material will cover in evening meeting on convoset/v multi file - there is an out for them on FAQ and Topic which won't have logging data to manually attach the datafiles in HF to try and trace back.
@dubois she was looking to move the meeting today to Monday Wednesday as we already had a meeting Tuesday Thursday.  Which is ironic, as she hasn't been attending the Tue/Thu often, and this meeting organised for Anand/Sam and they don't attend.  Anyway - said for her to counter to you as meeting organiser with Sam/Anand on and we'd try and work through.
She has an issue where she has invited the client to the Tue/Thu evening checkpoints making it difficult now to discuss some things she needs to so having a smaller forum meeting probably helps her.
Stephen  [8:48 PM]
The question we didn't reopen on the end of call is how for NBS calls
Custom error -> phones broker -> phones frontline agent -> escalates senrior)Is there need to be a broker error class.
We've tried to standardise across and with the number of calls and changes, maybe this is a bit blurry
@Nipuna you did a great job remembering it!
Not sure it's going to be worth reopening this one right now.Stephen  [8:52 PM]
Some really positive feedback from the Definity leader on the call.
TS - Tawsif Saleheen 36:57
Yep.
Kim Gregory.
Great job, right?
And this is this is really good to see.
It's really good to see the breakdown.
I think from the business side, I guess the only takeaway and we'll connect with regeneration on the side just to get a better understanding on the the runs for these sonnet outbounds and how we can use topic modelling to get like a bit more insight on that.
But yeah, other than that, like it looks fantastic.Stephen  [10:00 PM]
Deloitte have run into a couple of things

unlinking linking delay
they need to have complicated checks on whether things are finished.
Having talking thorugh they are more convinced to move to the recommneded design and are going to try to avoid the linking unlinking.
I think that is better, but will be put the focus very much on us if something there isn't working.
Sreyas checking Confluence/Sharepoint - and whether we need Definity things (edited) 
John  [4:44 PM]
@Stephen @Nipuna QQ re: timelines on Definity. When would be the best time to begin handoff/training to Shreyas and his team at Definity? end of September? Thinking week of 23rd Nipuna and I go down to Waterloo and meet them to do it in person.

Can you let me know if I've got decent dates/timing and I'll send the email out right away
Stephen  [3:06 PM]
John Norris
Fri, Aug 30, 4:00 PM (3 days ago)
to Zeeshan, Shreyas.Ragavan, Nipuna, me
I hope you are both doing well!

I've copied Nipuna and Stephne to this email as they will be critical in the knowledge handoff and training for your team. Shreyas, I understand you are attending the Tuesday & Thursday calls which is great. 

Here is a proposed approach to knowledge transfer and enablement:
Two to Three sessions remotely between now and Sept 23 for Enablement
Onsite week of Sept 23
Regular bi-weekly or monthly syncs
How does the week of September 23rd look to come in person? I'm thinking we can cover the following:
Knowledge transfer / Enablement
Establish Quarterly Business Review cadence
Use case roadmap
Alignment on outcomes for successful partnership
HF feedback / scorecard

Product Roadmap review + feedback
Let me know if that works and we can begin scheduling.No reply as yet, BH today, will check in call following.

@John Sreyas has taken away the action to try and workout how to best collaborate with humanfirst - do we need a definity logon?   Specifically a way to share files whcih we don't have.  Deloitte have access via a Definity logon.  We were given Deloitte logons which give access to a very locked down Deloitte area and no definity.  We can teams Definity via the Deloitte teams, but not share files or do a great many other things.
[3:07 PM]Joined the Deloitte standup which Sam requested and accepted but pressume not on because BH.
Stephen  [10:22 PM]
QA: https://tableau-uat.gcp-nprod.economical.com
UAT / Prod: https://tableau.gcp-prod.economical.com/

Ok had a really good with Shreyas working through a lot of things. 
Limited ability to look at the "other" categories and end to end monthly flow as 
he doesn't have access to the Tableau prod reports
datafiles for prod not there whilst conversion happened.
So we covered what we could
Fundamentals of revisions, cloning safely
Filter, Sort, Cluster
How to use uncertainty to investigate

Next sessions
Go through spreadsheet - share by email.

Other actions
I need to get an inability to create clone workspaces checked out - maybe permissions have changed?

Urvashi, Riddhi, Olivier not on - as "didn't have questions." so asking for us to use with Shreyas.  Then had questions about getting filenames so Nipuna fielded whilst I ran through
We need to get the API coverage/examples up - Nipuna solutioned for the one htey needed to get filenames during call.

All the prod data has been deleted, and they are going through recreating the integrations on FAQ
Callback has now moved back from Sept - 20th go live to Sept - 30th.
I presume that means some deloitte on site replanning has gone on - don't have any visibilty of.
Shreyas had very limited info - for instance not the production Tableau boards and was glad of the time - so think we were usefully keeping some presure of Deloitte team whjilst they sort the integration.Stephen  [3:18 PM]
Nipuna, Urvashi, Stephen.  2025-09-04 14:00

Timeline updates from Urvashi - she didn't know if going through change request, whether a paid for or at Deloitte cost change.  Directed to Sam.
They have delayed go lives by ~ 10 days so Callback from 20th to Sept 30th
The requirements for Callback seem loosely baselined, and so one reason is that they are adding more for when it changes in discussions.
Urvashi briefed that in draft it goes back again Callback to 18th October.
It sounds like they are working with the assumption of those new timelines.
They are redeploying tomorrow 5th FAQ to prod - so data should start flowing about - she didn't know if the DAGs (the airflow routes) would have had the convoset change in
Nipuna trying to build examples ahead of Maxime and Olivier on that, currently working on metadata filter download.
They are deploying Topic model to QA on Friday. There is no established acceptance criteria yet - Urvashi knows to push for one after the FAQ experience.
Topic is a simpler single class per model - standing by for defects and retest next week.
Sra is the more complicated one and then will be somewhere between Topic and Callback.
Riddhi will start on Data extract for callback on Monday 9th, so still expecting some data in the week but unclear when.
Talked about ensuring that the Deloitte staff are booked out with their resourcing teams for the new dates - loosing key people now would be critical - Urvashi seemed to have in hand for the extension.
Talked about new banking opportunity - Urvashi didn't seem to have visibility - talked about high possiblity to reuse the architecture, process and code into that -could start planning the tranisiotn of knowledge andresouce intot htat. (edited) 
Stephen  [10:03 PM]
Sreyas, Nipuan Stephen 2024-09-05
Deloitte team all ducked out and asked us to try and usefully help Sreyas.  They were redeploying topic model to QA
The data is still not reloaded in HF whilst they try and sort out the deployment, so there was limited progresss that could be made.
The more he steps about in the tool the more he sees the importance of organising it in a way he can follow it, and the importance of getting the incremental loads right as part of the project.
He was talking about manually leaving it like it is and then him trying to manually manage the files and convosets - it was unclear how this would work with the automated dags as well.
Also uncleare if it would ever get done.
He asked if we could understand which models were used where - we explained the naming standard, but as it's just a playbook id called by an external system, we have no accces to or confluence, explained we couldn't tell him which ones were safe to delete.
Deloitte really need to clear this integration stuff and get it running smoothly and then they can outline the delivered configuration, and he'll start feeling more comforable he can see the data coming in and out and interact with it.
We talked usefully about the model review for 15minutes - nad agreed next steps (emails and Excel sheets)
We talked about concepts of cycling files,a nd roolling windowsa nd did to some text file examples.
Sreyas then had some very good questions on quarterly mocel releases from the LLM providers.
Differences between likely prompt change frequency (low unless call shape changes) and calassification changes (higher - i.e seasonal classes etc)
Talked generally about that.
Can't make any progress on next report till data in.Nipuna  [9:21 PM]
Debug call with Maxime / Riddhi / Urvashi

Last minute mentioning they are seeing bugs after skipping past two touch points
Maxime had questions regarding how to filter the export pipeline results since current code doesn't support
Provided the new code since PR is still not in as a seperate function
Need to confirm that modifying the metadata filtering there will / will not override the existing pipeline metadata filters -- my guess is no since this is different from the pipeline filter itself but need to check

Running into GUI bug raised in QA that is not showing generated pipeline results -- LINK
Maxime mentioned running into seperate bug outside of linking/unlinking where the pipeline export returns an empty array despite waiting for trigger to finish and convo-set to fully link
Got what they were testing to try and repro -- mentioned will follow up after testing
pipelineId: pipeline-PKZISIEU4FCGDNRST6QCPGSE, pipelineStepId: 'pipelinestep-7HTKFODABVEU5EFWCO2KTDES', generationRunId: '117', playbookID: playbook-V3GHF5LYGZAQHO5STMZEXEGP



Overall they should atleast be able to change the architecture to support the link / unlink with the new methods so told to get started on that while I look into the two bugs.
Nipuna  [10:57 PM]
Ok did some more tests

Instructed them to add a "file_name" metadata to the utterances so you can filter. 
Maxime was caught off guard by this but I mentioned this was discussed last meeting that we need a metadata field to filter on output of the pipeline.
Anyways, they will now go through and make sure thats added to be able to do this 

Memory / GUI issue was solved by AP  -- might've been the cause of the empty array results (couldn't repro this)
Verified also that passing a metadata filter on pipeline output won't somehow affect the pipeline metadata filtering itself
Attempted a link convo set -> wait for trigger -> run two pipelines -> wait for trigger -> download and seemed to be fine on their dataset
Overall they should be unblocked now but 
let’s see on Monday -- think we need to encourage them more to be on the sessions to keep us in the loop to avoid these last minute changes. (edited) 
Stephen  [1:02 PM]
Thank you for jumping on this one @Nipuna and @appaquet

@dubois this is a good example of why EST support is so important to deal with the reactionary way Deloitte are working.

They are doing things which are very poorly advised.


integrating for the first time into production without testing it out on a test system (then escalating it's blocking production deployment due to them not testing it!)
scheduling a production deployment for Friday evening (especially one with untested code)
ignoring the prompts throughout the week to engage with how the convoset change was going as we knew it was going to be involved.
not turning up to any of the meetings where time from two people was provided to deal with this issue - instead sending Sreyas for us to occupy time and keep away from them - I get this is useful for them but the session was there to bottom out this convoset stuff.
dubois  [7:28 PM]
I agree this is not the right approach, let me talk to Anand and Sam
Stephen  [10:07 PM]
Useful go forward thoughts - as they dig themselves out of the project that will make the next project (i.e bank better)

can they baseline their architecture as a reusable framework they have skills in - i.e if they use airtable by default, they can baseline the architecture from this project materials, and create an internal system with their new license which reads calls automatically and consultants can get skills on.
what of their code is portable - can they take the DAGs and integrations built on Airtable and lift them?


From our side we need to invest in our API coverage in terms of humanfirst-module, the examples provided, test coverage as part of CI/CD and Id recommend having an example swim lane diagramme.  We've had to pull together a lot of things for them just in time.

CS team can cover in next Quarter if it's given priorities in OKRs and the CI/CD E2E environment sorted out this Sept.

Some of this is happening incrementally as we put the stuff built/and unblocked for Deloitte into the module and examples.  But to get it to be comprehensive it needs some focused effort.
Stephen  [2:08 PM]
OK - so maybe conflating two issues - the memory issue probably was stopping them getting results.
Maybe they were trying to load in the old (bad) way?

Then they were then looking how to do the full load

Currently can't see any QA or PROD files - so unclear where up to.
Nipuna  [7:19 PM]
Urvashi sending a strange email. There was no messages from Maxime/Riddhi after Friday mentioning that things were still broken so I'm not sure what she's referring to? Also no idea what the permanent fix she's expecting is?

Hi Nipuna,
Thanks again for joining the call on Friday. Here’s a recap of our discussion on enabling filtering for JSON filenames:
Option A: Nipuna provided local code for filtering, which Maxime will incorporate into his pipeline. The downside is that once HumanFirst rolls out a fix, this code will need to be removed in a future production deployment. As this involves rework and another deployment, we prefer to avoid it.
Option B: HumanFirst to provide a permanent fix. Could you please share an ETA for when this feature will be available in HumanFirst production?
Since this issue is blocking the testing of other defects, we’ll proceed with Option A for now. However, we’d still like to know the ETA for Option B to plan ahead.
Additionally, on Friday, we realized the issue was not with linking/unlinking conversation states. The real problem is a delay in receiving outputs from HumanFirst’s pipeline. Since the export APIs don’t work instantly, Maxime added a significant timeout in his pipeline (DAG) as a workaround. While this is a temporary fix, it should ideally be resolved by HumanFirst. If this is not resolved, we will continue to encounter missing data in FAQ report.
Path forward: To proceed with the FAQ report, Maxime will make the following changes to his data pipelines (DAG):
Replace the link/unlink logic and use a single conversation set, appending new data as per HumanFirst’s design.
Incorporate the filtering code for JSON filenames.
Increase the timeout to handle pipeline output delays.
 
Note: We’re planning for FAQ re-deployment to Prod on Thursday (Sept-12) 9am.
Regards,
Urvashi


Stephen  [10:24 PM]
Wrote some basic tests - consolidated PRs - Nipuna could you review please?
I'll try and get released tomorrow pre 09:00 EST with Fayaz, but don't want to risk messing it up tonight.
Code review threw up one change:
to be consistent with other things returning the list within an object it should return the file list directly, not ask you to navigate the object to the files property { files: [] } to get the list.
Line: 1068 of apis.py - field="files"
Should be a half a line change to swap to the new SDK for Maxime when released, but so forearmed.
If there is some reason why this doesn't work just update back again in review.


Nipuna  [4:25 PM]
Let me jump on call with Maxime
6 repliesStephen  [4:41 PM]
Cool - let me know whatever you need find.
Stephen  [4:46 PM]
We did a deep dive into the humanfirst-module with Fayaz in prep for this morning, so there are a variety of ways of getting Maxime faster what he needs without going through production PYPI.
Nipuna  [4:58 PM]
Agreed so the issue was his dataset didn't have any call data only chat data. A good edge case to run into now than later.

The 2 Pipelines ran fine but since each pipeline is filtered by communication channel = PHONE | CHAT. The phone pipeline had an empty result set.

As discussed and tested with Matt yesterday an empty result set just returns {'exported_at': '2024-09-09T19:33:54Z'} with no "examples" key. Maxime's code retried 3 times and since no example array was returned, it triggered an exception without even getting to the CHAT pipeline.

Net net solution is to consider after 3 retries of querying after pipeline trigger successfully completed, if the result doesn't contain "examples", then you can mark that example set as empty as it didn't contain data in the original convo set. Then move onto checking the CHAT pipeline which would have actually returned results. Maxime confirmed there would be cases that only chat data would be in the convoset.

Side note, he has correctly implemented a convosrc_filename property which he's reading to export the pipeline results at the end.
Stephen  [5:45 PM]
Great stuff.  Want to be good cop in the teams channel and give a friendly update?
Nipuna  [6:02 PM]
Yep already did Maxime confirmed working now!
Stephen  [6:04 PM]
Cool.  Nice job.  Ok so let’s talk through this evening about the test plan on QA


Stephen  [10:22 PM]
Talked through the architectural flow in detail screen first time - think they were digesting the concepts for real this time.
Had draft convoset corrrectly name with files on Dev - code wasn't finished, tests sets couldn't be found/didn't have right number.
Agreed in depth working session tomorrow at their convenience to step through every stage on QA to make sure it's working and exact numbers are there.  Olivier back and testing himself, he'll draw in.

Had a useful upfront talk about callback afterward.

A.A - recommended - one file per conversation do a prompt without refernece to previous call like SRA - meets their constraint on basically not changing anyting on their side
A.B - impossible - join real time from two different sets - we don't support - (yet) 
B - lots of work their end - create new convoset of concatenated calls.  


Riddhi and Oliver displayed very good understanding of the promtp strategy and business rationalie for A.A

Very rough low noees that we need to step through

What is happening within dag 6.
BQ -> JSON
 - last data set - timestamp of file.  timestamp is last converastion of the file
 - takes 400 calls.
 - sends to hF as JSON

Dag 7
- looks last data of last conversation bigquery prediction writen
- runs the pipeline - may have data or may not.
- 400 results
- three filter - predictate predicate filter -  pass in an array - objects - key name condition.
- if you have three files - it's three calls.
- write everything BQ

Missed call logic - they sound like they have a hard additional problem
- logic for missed calls - daily exports for five9 for missed calls.
- look back on Maxime - two strategies - end of day file.
- replace filename - delete - can't do as will regneerate everyting

lots of edge cases.
- push up one files into the naming strategy as you need - dribs and drab files
- could be 20%/30%!

They are trying to test tomorrow go prod Thursday again

this is enormously ambitious considering they are refactoring their fundamental logic and couldn't run it end to end yet 


To do that they are going to need to loop back on the deletion strategy and are not implemeting now
Stephen  [1:30 PM]
Really good session yesterday thank you - I've tried to write up the core logic for the E2E check on QA today.

If I've mis transcribed or misunderstood anything in the DAG logic here - please lets clarify and we can get it documented - as getting this right is what is going to ensure smooth running in prod.

DAGs 1-5 are independently running ingestion DAGs staging data (important pre-step didn't run through)

DAG 6
 - looks at last data set in BQ (from DAG 6 or DAG 7?) for the timestamp of the last conversation 
 - this date will be used on the upload file as the filename (seemed to be missing .json in Dev)
 - takes 400 calls at a time
 - Transforms to a HF JSON
  - includes the filename batch ID on metadata to enable downloading at a later date
 - Uploads the file to a convoset
 - For future release: should also delete any files desired to maintain a rolling window of data (not implemented yet)

DAG 7  
 - looks at last data of last conversation bigquery prediction writen
 - runs the pipeline on a convoset 
 - pipeline will check across all conversations in all files
  - where a conversation has a cached result - HF chace key is hash of prompt content and prompt settings
  - will only send those without a cache result to the LLM
  (If the prompt or settings change, the whole window of data in the convoset will be brought up to date by the pipeline)
 - DAG Downloads the pipeline result by querying the pipeline with a filter (using AND) set to the batchid/filename
 - if there are three files since the last run, will need to download each dataset individually (can't combine AND/OR)
 - API is as the GUI in functioanlity, just assembling the filers there programatically - can test out combos there.
 - When pipeline finishes will run any classification predictions on the output of the pipeline
 - Inserts the data in BQ ready for next run.

Tableau then looks at BQ results.

Future missed calls logic will be needed.
 - perhaps as high as 20-30%? in volume
 - can't overwrite file - convoset will raise error because has dependent objects
 - can delete file and replace - however will cause the whole file to be reprocessed
 - has a lot of edge cases and need to look at five9 strategies.
 Two suggestions in call
 - can push up files whenever needed even if number of calls small as long as they fit in the naming convention and logic for DAGs clearly 
 - could future date the calls to push them off to a more convenient time
has context menuStephen  [9:15 AM]
Hi Stephen, thanks for the recap. Some notes for you and Peiris, Nipuna : 
DAG 6 looks at the last datapoint uploaded in the last DAG 6
In DAG 7, the current logic is to trigger the pipeline as many times as there are net new (unprocessed) file sets, each time with a metadata filter on the specific file set name. We then grab the results from each run and iteratively aggregate them. 
I've tested this logic and it's working well in dev. I had to fix something in the aggregation to prevent each pipeline run output from overwriting the previous run outputs. 
I'm now fixing another bit of logic in DAG 7. We currently rely on the earliest** conversation ID for which there is no predicted insight to start our search for net net file sets, but this logic is not robust enough. Sometimes the insights pipelines produce no outputs for a given conversation ID, which means it would forever remain the earlier datapoint without a prediction.
 Here is an example of a None output from the FAQ pipeline for a specific conversation : 



 I think the easiest strategy for now is to change the HF lookup logic. Instead of using the earlier convo without a prediction for the file set search, use the latest convo with a prediction instead.
 Thanks for the recap Olivier. Glad to hear the refactor is going well. So if I'm understanding correctly, if the prompt outputs "None" as FAQ's found, there is no prediction (Main/Sub category) written to BQ? This then means that if you check for the earliest convo set without a prediction, it could pick up on a date earlier than the last file actually processed causing un-nessasary reruns and re-writes and remaining that way indefinitly right?

So checking the latest file with prediction would work I guess. You could also write no FAQ generated cases with "N/A" as field in Main/Sub category so there is always a prediction if a file was processed regardless & then exclude that in Tableau end. 

I know we're not going to have time remainder of today but if you want to run through end to end tomm morning once you've got the changes made that works for me!
 Yup, you've described the problem very well. I'll see which solution is easier to implement! It might be easier to opt for the latest file logic instead of ensuring across all pipelines (Faq, topic, sra, etc.) that we always write predictions for empty results.
 Btw on this point if I'm understanding correctly this could be improved:
the current logic is to trigger the pipeline as many times as there are net new (unprocessed) file sets, each time with a metadata filter on the specific file set name. We then grab the results from each run and iteratively aggregate them. 
If all the net new files are already attached to the convo-set already, a single pipeline trigger will run all of the net new files (old will be pulled from cache). The iteration would only need to happen at the export result stage where you can make X calls to filter by each new file name.

Process:
Bunch of unprocessed files --> Single pipeline trigger --> Pipeline will get outputs for all unprocessed --> Let finish --> Iteratively call the export query on the single generation run ID per filename

If you do an individual pipeline trigger per file, the caching would work and essentially all the new files will be processed on the first generation run, and every subsequent run would just use the cache. Its just more API calls for no reason thats all. Hope that makes sense.
 Yup, that makes sense, thanks. I'll evaluate the amount of work required for that.[9:17 AM]Great work helping Olivier think through this and make progress @Nipuna - and great it's happening in the public channel so Sam and Urvashi can understand what's being worked on and see how we're continually trying to help them solve their problems.
Stephen  [10:02 PM]
Super productive call - 2024-09-12

Maxime on holiday - everyone on, with updates - just such a change.

@Nipuna and Olivier been setting up for success - sounds like Oliver almost has it working in Dev, and working properly.
Riddhi made some very sensible decisions on the convoset side - they should only store the data and filter it once.
They have put their production deployment off till Monday - hooray - no trying again on Friday night.
They haven't yet managed to deploy to QA - the definity CI/CD enviornment sounds hard.
They are sticking to the end to end walk through plan and testing on QA before live - oliver/nipuna going to try that tomorrow.

Archiving
Sreyas wants to archive all the JSON into GCP somewhere - fine - either he downloads or he will raise ticket for Deloitte to write it somewhere when they have that DAG transform it.
But it's just a copy of what's in bigqquery anyway so seems a little pointless (if convenient for him to be able to load manually if he wanted)
Olivier thought it should be straightforward (and it should be), but we all pointed out that it'll be big, and they need to plan for data retention policies etc etc - leaving it for definity to work out.
That could be 13 months
For rolling window in convo set they need to work it out, have said DONT keep 13months, keep a sensible rolling window like 30 days, 90s top.
Going to plan out what limits and data looks liek when catchup happens.

Catchup
Turns out they are running DAGs every 15minutes in order to catch up the load from June 19th - so we are going to see rapidly datasizes and performance challenges if any.
Once caught up - they seemt o be open to going hourly.
Aim is starting that next week, with alerting on every 15minute job starting shortly after.

Operability testing
Explained memory errors
Talked about Anthropic outages.
DAG failures.
They don't know who is taking on DAG maintenance yet.
Doesn't seem to eb an operability test phase planned.
Definity wanted us to plan and run - we pointed out that whoever taking on running the jobs and maintaining the DAGs needs to plan and run that.
But we would help participate as part of support if they wanted us to kill pipelines, or similate a anthropic outage if they planned and commuicated.

Data storage
They have worked out how to store everything just once and use pipeline filters on everything!
So expecting 3 convosets Dev - QA - Prod
Then 12 worksaces 3x4 reports and pipelines pointing out.

Data limits
Reminded on SRA 1M convos.
Explained soft limit 20M DP limit.
Going to plan out based on rolling windows and catchup how many DPs that 1M convos is actually likely to be.
May need to take some planning of hardware when that is there.Stephen  [10:08 PM]
Copy of email and what on teams.
Ok - I see an email chain as well with Mathieu as well today. Catching myself up.

It looks like there are two things raised.
1 - a pipeline failure with a 403 RBAC error
2 - timeouts when downloading large 

1-pipeline
Will get the dev team to look at what happened on that run.
In the meantime can we step through how the error and restart logic operated please?
My understanding would be that the pipeline will have not executed, and then the next batch run should have picked up that data and it should have succeeded?

2-For the HTTPS timeout 
If you are trying to download a large amount of data it might well take longer than 10s with batch predict
Adjusting that via the SDK can be done via the cfg file
https://github.com/zia-ai/humanfirst-module/blob/master/humanfirst/config/setup.cfg
Is this viable for you to update here as this is available right now?
If not can talk through how/why not and we can work another way of making it adjustable for you that will fit into the way of working. Overriding the cfg value with an Environment variable or introducing an overridable default parameter on each function might be options.setup.cfg[humanfirst.CONSTANTS]
TIMEOUT = 10
EXPIRY_ADDITION = 60
TEST_NAMESPACE = humanfirst-academy
TEST_CONVOSET = humanfirst-module-testing
 zia-ai/humanfirst-module | Added by GitHubStephen  [10:14 PM]
@fayaz first thing IST could you have a think through 2 please.
I've had 10s not be enough when I was batch predicting a lot with the HSN work pre pipelines.
Is it viable for them to update a PYPI installed module cfg file - I guess you have to go into whatever venv etc, and replace this value?  I don't really understand the DAG Airflow env they are using - or how much python they know?
Assuming maybe it isn't easy to update this value, could you code  away for an SDK release tomorrow that is.[10:18 PM]Oliver:
Thanks Stephen. Issue one is indeed not a blocker, as we can simply re trigger the pipeline in the following run of the DAG. For option 2, you mean customizing the human first SDK? Or is there a way to point the SDK to a custom config file ?(edited)
mathieu  [12:00 AM]
issue 2 seems easily solved by having a retry annotation on whatever they are using to call into the api, it’d be a more resilient to network issues (and there’s no reason to fail the whole thing because a single api call has a network issue)
Stephen  [12:15 AM]
Yeah.  Also batching/chunking there is always going to be an upper limit to the feasible side of the batch.  Stuck it in Deloitte Teams Channel with examples and giving them the timeout override now anyway. (edited) 
Stephen  [12:26 AM]
@fayaz ended up just writing what they will want as well as sending them what the needed to do.
Added some tests covering some more areas whilst I did it.
As optional parameter seems very safe for the user base as you can just ignore it and already at the end of argements.
Could you review, adjust as needed, merge and deploy 1.1.4?

Stephen  [3:03 PM]
Our useful lessons.

Coverage and testing of APIs
Example Architecture needed.
Claude Sonnet is friendly work with for these cases.
Proving quality of prompt output is hard in tool - dropped to spreadsheets a lot (with a lot of python)
That proof is necessary for acceptance by client of output (ala Nesto, and HSN etc)
Incremental loads are hard for our clients - having that logic built in useful.
Operability and recovery modes critical to the final client.
Breaking BatchPredict into manageable batches
Breaking pipeline downloads into manageable chunks with filters
E2E - File to insight logic would be useful.


Deloitte useful lessons

Manage your holiday plans along side your project plans.
Make sure you back off R&R with your suppliers and client and do proper contracting.
Review the plan with all parties to check alignment.
Do realistic estimates of fix and development times, not just a day for each stage.
As a system integrator the architecture diagrams and swim lanes are your primary responsibility - don't avoid them - keep them up to date and in front of people.
Access and co-operation is key - members without machines or access makes things hard
Turn up to sessions.  We're there to help!  Let us help!
Whilst we taught them HF - I think they have also learnt a lot about Airflow - pick a preferred ETL platform.
Be data driven - don't to start phrases without it as it build in bias you then have to rectify later in the project.
Don't skip testing phases and go to prod when you are under pressure.
(edited)
Stephen  [3:11 PM]
Typically behidn tableau on a data lake - a big repository of data with all sorts of different tables of information from HR, Finance, Sales, IT, this system that system etc…

Tableau helps you turn those tables easily to combine data from different departments into charts and dashboards which you can interact with to get insight.  So show me the top products we sell in Michigan and what’s the margin we make on them.

Currently their conversational and document data is opaque to those companies.  They can’t answer questions in tableau about what happened in a conversation or why something cost twice as much in that contract as last year. 

Humanfirst integrates via its APIs with the ETL (Extract Transform and Load) (airflow, snowflake, BigQuery whatever) to pull out the documents audio and conversations out from the datalake and push in rich insights that are then automatically available to tableau. 

So you can go to saying.  What’s the top FAQ i could build on my website that would deflect the most of my call volume.   What tactics are my top sales agents using in calls.  What are the key driver of increased cost in the contracts that are reeducinh that margin in Michigan
[10:56 AM] Stephen

So net net we integrate with ETL and the datalake then it’s available to tableau, not directly with tableau.

[10:57 AM] Stephen

The other product talks about being more pipeline like raw data to insight.  I’d have to research to give you a specific answer.

But in general the above applies to visualisation products like Tableau and Looker

Something Ange asked "how do we integrate with Tableau"

Stephen  [11:13 AM]
Couple of emails sent out short summary here.
Deloitte 3month password change locked me out
Have asked to put our humanfirst emails on the daily summary - the collaboration tools are just not functional - we also need to move away from Deloitte systems and work more directly with Definity.
I have headed off the existing bugs.
I can't make tonights meeting.   Nipuna will leave it in your safe hands. You've got the callback initial work to set reasonable timelines on for next week.   Then any walk through with Olivier of what is happenging with Topic/FAQ combined.
Really that is the only thing that matters for success of all parties, and Deloitte haven't reached yet the point of actually testing it - so helping them just survive until they can do that, and then making sure it works is the order of the day.
If Sreyas or Urvashi are pushing on spreadsheet review, bug walkthroughs, handover etc - anything else not directly related to process please feel free to deflect to me and point to the Monday 09:00 EST catchup to resolve. (edited) 
Nipuna  [10:24 PM]
QQ @mathieu I would test this but sorta need an quick follow up for Deloitte. They are asking what happens with pipeline caching in this scenario:


Initial file1 in convo-set loaded into tool -- has 4 conversations with 4 unique convo ids
Run a pipeline on that convo-set -- Get back results
Delete old file1
Push in new file2 with 2 of the old convoids (same conversation) from the old file, 2 new convo-ids (new conversations)
Trigger same pipeline


Expectation:

Given prompt or pipeline settings haven't changed, hash remains same for the two convo-ids from the old file1 so it references from cache and pipeline only runs the 2 new convo-ids
(edited)
Nipuna  [11:42 PM]
Long long day with Deloitte dragging on but recapping before signing off:

Timelines
- Push back of timelines for about 2-3 weeks in general (including FAQ deployment)
- They are refactoring the code around the look back mechanism due to five9 missing calls issue. Five9 will miss calls frequently, and need to catch up at the EOD. Business wants regular intra-day processing (multiple times per day) rather than just running one at the EOD accounting for all the missing calls to come through. Olivier / Maxime changing the code to meet - not rly our problem but they need to solve.
- They've also decided to do lots of tests in DEV themselves, before moving handing off to the QA team and so they've gotten time to do that - which is great. Olivier mentioned the refactor was why the e-2-e tests weren't happening and these could take place later @Stephen
- Seems like this decision was made to prevent push back after push back and just have time to actually test everything end to end

Callback Report

Worked on for 2.5hrs to do some initial data discovery and showed initial categories via discovery
Needed to tune prompt to really not converge in on what the topic model report already provides
Otherwise prompt would say Callback about Policy Issue -- when thats not what we're looking for

Using no dataset filtering logic and just trying to identify callbacks brought up some interesting cases which I raised with the team
Immediate agent to agent discussing a call switch over
Callbacks due to calls / chats disconnecting
Agent outbound callbacks due to requested escalations

They agreed that all of these cases cannot be excluded so added a few categories to match
Their checking with business on the initial list to align if these make sense in terms of what they are looking for since there exists no baseline
Urvashi / Riddhi and Miguel (PM) all seemed to agreed on the initial list of callback reasons 


Caching 

Question was raised on the scenario above / Riddhi was trying to do a test
Matt helped clarify everything and we did a test with 400 calls in one file and 401 calls in one file, one ran after the other, and the pipeline cached the initial 400 and inference the single call - saw on GUI with all 3 of them on the call
Also pointed them to check their API calls counts on Vertex if they needed further clarification
The discussion around caching came about b/c of the five9 issue where the EOD might include some re-runs of calls that were missed but also calls that were already processed. So it was a matter of Miguel / Samantha trying to get a grasp on if extra cost is incurred
There was some q's around if the next step of extra batchPredict calls would cause extra charge -- mentioned not likely going to be the case but Miguel checking with Zeeshan on contract details (might come up on Monday).


Shreyas

Shreyas had questions around how to evaluate hallucinations without manual review
Tried to give him and answer and swayed we can discuss in another meeting
He's got the Excel sheet (shared with us) where he's logged questions that he has and wants answers eventually when the hand over process happens
CALLBACK_REASONS_DISCOVERY.txt 

Unfulfilled resolution follow up
- User is following up because the resolution or action promised in a previous interaction was not met, and the issue remains unresolved.

Clarification on ambiguous instructions
- User seeks clarification or further details on instructions received in a prior interaction that were unclear or confusing.


Stephen  [9:23 AM]
they've also decided to do lots of tests in DEV themselves...why the e-2-e tests weren't happeningThis has always been the point of encouraging them into e2e test to educate them that they had to run it through themselves in dev to understand it and successfully code it, before shipping somewhere.

Also why we pushed back so hard when they tried to get us to skip our testing phases because it is never an accelerator.  As a system integrator you are responsible for quality gates which ensure the end to end solution, you can pressure a supplier to complete their testing by a certain day, but telling them not to do it is madness

Glad they are finally getting it.
[9:25 AM]decision was made to prevent push back after push backMost troubled projects eventually come to this realisation that making unrealistic waterfall knock-ons - i.e the 1 day to dev, 1 day to test, 1 day to release, end up in the weekend - ultimately tend to be much more embarssing and painful on the team than facing up to the issues and replanning based on demonstrated velocity.
[9:29 AM]Five9 will miss calls frequently... Business wants regular intra-day processing (multiple times per day)This is a major scoping and architectural gap that has been known left to fester, it's unfortunately now going to bite them very hard.  As it's so fundamental it should have been dealt with up front, even though that would have appeared to slow the project.  The refactor for this is going to be very hard for Deloitte.
Stephen  [10:34 AM]
Moving the crucial bit from the longer thread about removing and adding files to the top here  (TQ Matt)
the cache is based on the rendered prompt content and prompt settings. As long as these are stable then you can delete/re-upload as much as you want and it'll be cached.So basically now they are adding and removing files not convo sets we should be OK. (edited) 
[10:36 AM]initial list of callback reasonsThank you for your work on this @Nipuna I think it really helps them get ahead and show the client progress as well as insight on the problems they'll face.  Can you post the initial list here we've given them?  (Apologies if I've missed it elsewhere)
Nipuna  [5:27 PM]
Hi @nipuna@humanfirst.ai,

Thanks for helping us verify the cache with Vertex AI yesterday with @Dasani, Riddhi

Hoping you can get back to us asap on some follow-up items as this will inform the direction on the project.

Now that we’ve verified this. We are trying to price out the option of running the pipeline again with a few updates. This is because there are some conversations that are missed throughout the day so there has to be a “catchup” job run and instead of trying to figure out deltas, it would simply our architecture a lot to simply run the job again with the calls.

Seems yesterday we verified that Vertex AI calls are cached but the topic model calls are not cached.

2 questions I wanted to follow-up:
Since the NLU model is only trained when we decided to train, I’m assuming the re-running of the conversations against the model should deterministically be the same result each time
Speaking to Definity, the contract is priced according to “interactions”. If we re-run some conversations and it hits the Vertex AI cache and the NLU model, does that consume those “interactions” in the contract?
 
Cheers,
Miguel

Ongoing discussion between Miguel / Samantha around the batch predict pricing concerns. @Stephen going to CC you into this email.

On the batchPredict NLU calls, my understanding is they are deterministic if the model has not been retrained in between for the NLU right.
Stephen  [5:31 PM]
There should be no batch pricing concerns - say you think it’s fine send to me to deal with and I’ll walk through with Sam on Monday.

Also you can suggest that the pipleine download already has that information which may let them simply and avoid these steps if they want.  
[5:32 PM]On deterministic - your understanding is same as mine - you can test in the GUI using the tester.  But between trainings even if identical training sets it will differ slightly
Nipuna  [5:46 PM]
Ok thanks for clarifying, email sent, CCd you and Alex
[5:48 PM]Btw on the call back reasons I added .txt file above but think its missing the last two that were added after the discussion:


Alex followed up on billing question.  I followed up with batchPredict might not be necessary.  I think it may also end up be necessary due to one pipeline wanting the result from models in two differnet workspaces, one for NBS and one for Sonnet.

Cool. Yep running multiple batchPredicts when needed isn't a problem. Something else that might help is that is when the classification model is in the same workspace that the pipeline runs in, then the pipeline download it should already have the prediction for the output on it in "top_matched_intent" - this may mean you can ommit completely batchPredict steps.

The only reason why a separate batchPredict step is necessary is when the output of one pipeline needs to be evaluated by multiple other models contained in different workspaces. For instance if the pipeline is produced in one workspace, then evaluated for Sonnet in another workspace, and NBS in another workspace.

If the pipeline can be run in one workspace for Sonnet (pipeline with model in) and in another for NBS (pipeline with model in) both the pipeline results will automatically contain the same information a batch predict would

Nipuna  [3:44 PM]
Hmm good call out I also spent some trying to understand that logic. I don't think the BQ table gets updated until the full lookback period is complete. Meaning the BQ table will always be 24-48hrs behind to prevent the scenario you described. I think the Ingestion DAG1 isn't running every 15 mins either like the inference DAGs more like every hour / or twice a day. Just guessing, could be wrong though. (edited) 
Nipuna  [10:07 PM]
EOD update: Got the test team results from Riddhi late afternoon for English. Got it mapped back to the prompt results. Most of NBS seem to be correct, test team has just identified calls that shouldn't be callbacks (not_callback) that will be handled via post processing (not fault of prompt).

For Sonnet, there are cases where the prompt isn't matching the expected output they've outlined. Read through a few think can solve with some better instructions. After quick rebaseline through these are rough stats. Will pickup on Monday on some prompt tuning. (edited)

Stephen  [9:52 PM]
...Discarding a key system response with no record of it having happened is sort of ridiculous as a System Integrator
Trying to give Deloitte some cover by explaining that there are probably (confirmed there are) airflow logs and explaining how Definity can configure control M alerts checking numbers of these.
Ultimately it's not really probably an issue as there will be lots of no predictions for some reports, so if the error rate is low (which it should be) there will be no impact on the graphs, and in the practice few to little alerts.
Also trying to remind Shreyas of him actually preparing his operability tests - as likely no one will unless he plans to conduct that.
Managed to get that walked through to a level of detail where everyone seemed comfortable.
Shreyas still wants it logged somewhere he can find it (which I get), but somewhat reassured.
Then they can go into HF for the window and see those clusters of failures well there.

In terms of the refactor - maybe it's ready for Dev testing on Thursday.
Urvashi didn't know if test team was preparing test data for missed calls - which is worrying.  Suggested that was probably key to test this refactor.

Voiced that everyone nervous until seeing multi report tests on single convo set with the refactor.  Can't really address other client questions without that in place


Stephen  [10:03 PM]
I hope they can get the code onto QA soon.  These pointless questions about worrying hypothetical scenarios and what the code might or might not do,  when we can't actually see it doing anything is getting tiresome.
Nipuna  [10:12 PM]
Yep its turning into a never ending list of hypotheticals :sweat_smile:
Stephen  [9:30 AM]
You're doing a great job keeping us ahead of the curve on Callback thank you Nipuna.  Whilst we can consider their suggestions for the test, if you're running it and it doesn't make sense - we've laid the stage yesterday for pushing back and doing the right thing.Stephen  [10:00 AM]
Shreyas Ragavan (External)Broadhurst, Stephen, the Excel sheet has been re-shared.

Stephen: Thank you - looks like access expires after a certain time or action.  Once reshared I could easily get back in.  All HF dark blue items addressed, tried to close as many as possible.

Some call for deep dives on certain actions.  Once code is up and running in QA on all four reports on the single convoset and the confluence is in place documenting the envrionments it should be possible to repurpose one of the two weekly sessions to start covering these.  They can work up through the creation of a new namspace, the copying of a test data set, prompt creation, and classifier creation from scratch and then using the SDK from scratch.

Stephen  [9:41 PM]
This one - 7a494ad3-c163-52c9-b417-7d344651471e-COnversation ID
Definity asking why previous no runs - said they won't see that them.
Did appear in the pipeline we see in humanfirst.
They see the data in metadata that the prompt ran
No results though NA[9:44 PM]Olivier now on holiday.
Olivier did the topic prompt design and has done a very complicated INTENT/REASON paring through the conversation, so there are multiple through there. (This was against our recommendation for having a single Topic per call)
This then means that using a 0.35 confidence they are going to have loose categories.

Looks like the nbs dev sonnet when rushing they left some categories as single parent single child  "Renewal" - "Misc. Renewal"
Which isn't very satisifying and the  usiness complaining.  Asking us to go back and look at possible subdivision.

"Driving History, accidents & claims" - Tester (Rakesh) not clear if this was as history includes accidents/claims

This though just feels like a timeout - espeicaly as they are at the bottom of the intent list in the dev environment.
"Renewals.  Misc Renewals."
+ "Misc. Quotes"

Great and the good were on Anand on camera off in the background.
Sam camera on unusually.  Did some useful pushback on signed off data. (edited) 
Stephen  [9:59 PM]
Rohan still testing the combined new logic - now Thursday tyring to deploy on QA.
So current testing on FAQ and Topic being done discretely and on the old dags.

Stephen  [6:04 PM]
Urvashi pleased with how we did with HF presentatio now asking us to present topic report - this seems inappropriate.
They're also pulling forward meetings due to their team changes when there are likely to be large changes and we still don't have an end to end test on refactored code.  I am pushing back
Agreed, the KT went well yesterday, thanks again for presenting! I would like Nipuna to attend the KT calls that Riddhi leads, so that he can answer any HF related questions directly. I'm also thinking it's best if Riddhi presents FAQ, SrA and CLB, and Stephen you can present TOP, as you were more hands on with it. We can do TOP KT on Oct-23 (Wed).[6:04 PM]Plan is for QA team to start testing FAQ report E2E from Monday Oct-21, we are testing couple more things in the refactored code today. There is a requirement change requested for FAQ (include count of NAs, low confidence score on dashboard), so we're working on implementing that as well.

Rakesh (QA) has completed first round of UAT of FAQ, and will be sharing the details with us today, but here are the numbers he shared yesterday evening. I would like to discuss in our Touchpoint with you today, how we can improve the accuracies. It's at 84% for Sonnet and 70% for NBS.image.png [6:05 PM]My response
Just to correct there, I was not hands on with Topic this was written by Olivier - particularly the choices around the complex multiple class prompt layout. I did help with one of the classification models on the prompt output, and have updated now the Olivier did to clear out the unfinished "Misc." classes.

If you remember at the time my explicit recommendation not to include this multiclass and that laying out the INTENT, REASON, JUSTIFICATION, followed by INTENT, REASON, JUSTIFCATION within the same prompt output would very probably lead to a lot of difficulties getting through QA.

This is because it gives a) it gives much greater range of ambiguity for the test team to select from, and a much higher number of possibilities to have to match to get a "PASS", but also b) because it is going to be much harder to control the prompt output and consistency, and c) the outputs from the first class in the prompt will affect the behaviour of the second which makes it even harder to predict

Having ignored my guidance and gone about in a different way - I don't feel well able to represent the design decisions behind that in a meeting about the Topic report. Especially in the situation where we're going to present a solution that there is a reasonable chance needs a large amount of rework to reverse some of those design decisions if the QA requirements can't be met (though I understand they are looser than some other reports with "most being met" in the top quartile)

Also having reviewed the prompt there are probably already a set of prompt updates that need to be done to accommodate the swap from Gemini to Sonnet which was done at the time, and look at overall prompt run consistency.

We're only now getting to the point where we are getting clear FAQ feedback which is great we can look at that.

But we don't have the Topic report QA yet - or is this available?

So overall I feel this meeting is too early to be presenting the report in detail when there may need to be major changes in both the way it works and the logic of the output, and where we haven't achieved an end to end at all on the refactored code.Stephen  [8:58 PM]
@Nipuna I'm just logging into the call.   It looks like Rakesh has the first set of proper feedback.  He's going to want to present and talk fine - but really we need the full sheet to give any realistic answers to anything.

Lets not try and solve them infront of them rather listen, get the detail, go away and look and comeo back.
Stephen  [9:59 PM]
OK - so quick summary call. First section answering Shreyas explaining how to download the predictions along with the pipeline results in tool, when they were batch predicted rather than taking off pipeline, how to tell which NLU default, and which version latest.  

Then onto FAQ results - business and Rakesh generally seemed happy, but queried 7 calls where they thought there was hallucinations. Looks like some parties listened to call, others skimmed transcript. So question is are these substantiated from the call, or is there a hallucination - we'll have a look through.Nipuna  [10:39 PM]
I reviewed the 7 conversations mentioned as hallucinations in that spreadsheet and added the reasoning and the snippets. Overall pretty much all of them seem to just be heavily inferred questions that however are valid questions a User might face related to the context in that conversation.

I think with the snippets and the reasoning, its very easy to see the the links. Also given the nature of the report and the prompt specifically being called "Inferred" FAQ, I don't think these are too worrying.

I attached the spreadsheet with the notes I made. On a separate note, it is super valuable to have these snippet/reasoning to go back to review and worth keeping in all prompts even after the initial development. (edited) 
Excel Spreadsheet FAQ_Business_Review.xlsxExcel Spreadsheet[10:42 PM]This is an example of one - The green are the valid. For the hallucinations: One question was inferred from the agent utterance and the other was a direct question asked by the User to the agent that was generalized into a potential FAQ. (edited) 
image.png Nipuna  [5:01 PM]
FAQ KT session went pretty well overall. Riddhi had prepped nicely and confluence page was well documented. Answered a few questions from Shreyas and AA team regarding model predictions, prompt parameters. Few questions regarding architecture on import / export logic pushed to other DAG specific KTs. Urvashi brought up the UAT results as well. Next one is SRA on Mon 21st. The separate session with AA team / John and myself seem to be helping them understand the platform too. (edited)

Stephen  [10:34 PM]
90min call with Definity Sreyas Rakesh and Deloitte
KT running ahead of actual delivery and loosing Oliver/Riddhi creating a lot of risk.
Definity asking the right questions, and spending time understanding the answers - was very collaborative.
Buit large numbers of worry questions/misunderstandings on how particularly Topic (the Deloitte delivered report - also the most signficant for "what is coming into the call centre") will work.
As no-one can actually see it on any environment yet - it's all so theoretical and everyone worried about signing off because it might not work for them in practice when they do see this data.
Deloitte have let this Topic report get extremely complex, their prompt standard/consistency are loose, and the client clarity on expected behaviour is loose.
Maybe it goes through test and all works, but my feeling is  there is a high risk of substantialrework when they start seeing results and interacting with data.
Having rolled off the key resources and replaced with someone Junior this is worrying.
Urvashi was starting to try and set up us in case Rohan couldn't field questions had Nipuna had KT from Riddhi on everything he needed.  I have already pushed back on this, that they have to conduct their KT to their resource, the KT isn't Deloitte->HF it's Deloitte -> Deloitte and we will support either Deloitte and/or Definity in any questions on the platform.

But net net is this is set to run for a while and still need a very high dependence on us.

Stephen  [12:22 PM]
The list from the business seems to be a very wide ranging set of requests for the Topic report, which could have impacts across the Prompt design, the DAGs as well as the resultant classification and potentially the dashboard.  

For instance some of them are not looking at the intent of the customer "switch to another provider" but whether that churn successfully prevented or not, which is likely going to need dedicated separate conversation analysis and I'm not sure how would fit into the dashboard

Mishra, Urvashi I can give you some commentary on it, but someone from the Deloitte team is going to need to review this in detail against the previous requirements and agreements and determine what is reasonable to attempt to adapt to whilst considerintg the project timelines. Who's best in position to do that please and I'll forward my commentary to them.
 You can send it to me and Riddhi, we will review it together. I have already informed Business we will not be able to incorporate all requested changes, so as long as we can provide good reasoning we should be good. Also, for the ones we won't be able to do, we need to write up the steps to be taken to implement it after Go-Live. We will only make model enhancements, which can be completed by this friday or latest by Monday (Oct-28)
 Some quick effort estimates.

Go through each model/contents with context of data already in workspaces and make recommendations. 60-90minutes each, 
there are 4 models commented on in the sheet.  

Update just the renames, splits and requested explanations in the classification model only with no prompt updates, then tune and retest the model back to similar performance in dev ~0.5-1 days work per model.  

If prompts need to be updated to add additional specific insight for the different models - for instance the difference between primary driver and named driver, and highlight province issues.  ~2-3 days work per model (assuming only two models here as Intent/Reason Theoretically combined) to update prompts, rerun data, and rebuild models.  

In doing so we are likely to face issues that the prompts need to be updated to the latest Anthropic standard and better aligned in their behaviour.  That may lead to more rework.

It may well be necessary to have more data than has previously been available to get to the level of granularity that is being asked in some of these

Urvashi
 Thanks for the effort estimates Broadhurst, Stephen. Here's my plan, let me know your thoughts.
Focus on topics/sub-topics for Sonnet & NBS - Implement the ones which are straightforward (renaming, splits), and answer questions on the excel. This should be done ~2 days according to your estimates.
You can then add 1 contact reason requested for Sonnet. ~0.5 day since you were the primary owner of the NLU model.
We can revisit NBS contact reasons next week. I will push back on this, explaining the dev changes needed and also that this list was finalized way back in August.


CC Chan, Samantha Peiris, Nipuna

Stephen
 Pushing back as finalised in August is a good idea.  I do not believe though that the client is going to be content until they can see it running at volume on QA - a lot of the contents are expressions of worry and misunderstanding of the report.  Without being able to see and feel it I understand where they are coming from.

I am not the primary owner for any of these models - I stepped in to help Olivier when I returned from Vacation, and again recently to help complete the subdivision on Quote/Renewal he had not completed on the original model.  Deloitte is the only owner of this model delivery.

The testing procedure we've pointed out repeatedly as extremely necessary on the other reports like FAQ, and you were eager to skip on  to make progress then, does not appear to have been done for this Topic report.  I've received the spreadsheet of unformatted data - I can't see any summary to the client of the numbers or the quality - if this exists can you forward please and we will try and advise how to better remedy.  If the report was finalized in August then this testing would assumably been the basis for it - if that is missing it may explain the gap in client expectation.

My estimates above are estimates for a competent person to complete - not an indication we were doing this - you appear to be assuming we're going to engage in further unpaid professional services to complete the above work as Deloitte rolls off the experienced resources (abet for good personal reasons).  Can we table this for next week as the integration caused overruns and the substitution for Deloitte resources are now becoming too great for us to continuing to swallow without consideration.

We are going however to try and do everything we can to help you maintain client confidence here and let you finish the refactor work.  I repeat that a joint E2E test of that with multiple reports on single convoset is going to be crucial to project success - this is still outstanding.

I've pulled Oliver in my team off other activities and he is working through today on the Sonnet model.  He's concentrating on implementing what he can from the list without updating the prompts.  Explaining some of the others with examples and conversations that you can take the client through.  He's going to start with Sonnet today.

We will try and come with examples of that work this evening to see how that's shaping up and what it means for the remaining plan through NBS.Stephen  [7:10 PM]
KT session started - Deloitte sharing on Topic - going into the multi classes and this is the target diagramimage.png Stephen  [7:11 PM]
Sonnet Intents Split end of day update

Oliver has worked through and we've the key additions. Generally concerned that model to date appears to be built on a variety of different datasets, prompt runs and potentially prompts.
Those change quite significantly the outcomes for things like Vin Decoder and slowed us down a lot as the decisions become not clear cut because it depends on which version of the prompt/data is in place now.

 I'd recommend running an entirely clean pipeline against the current source controlled prompt and data set and then check against that to be sure of the results expected in QA.

Further details on other things that aren't addressable we are still updating the XLSX sheet, but the things we've been able to address today without touching the prompt are.

Added/Split
 cancellation / policy_cancelled_by_insurer
 cancellation / cancellation_warning
 cancellation / confirm_cancellation
 cancellation / questions_about_cancellation_process

Split this to two
 customer_support / login_access_issues
 customer_support / website_issues

before 46 intents 91f1
 after 52 intents 89f1

Can we step through in the 20:00 GMT / 15:00 EST today and work out where best to go next.


Stephen  [9:34 PM]
@fayaz could we try and pick this up  with SDK 2.0.0
For SDK 2.0.0 can we have every function call for humanfirst accept an additional optional parameter of timeout=
Like the one we did for the one function.  So Definity can override the timeouts on any function - not just the one function we already did this for.
Can we also up the default from timeout = 10 to timeout = 30 in the CFG file.
And check that there is no rogue TIMEOUT variables elsewhere over riding.7 repliesStephen  [9:38 PM]
Sreyas talking a lot of sense on this call.  Maxime either dissembling or failing to make himself understood well.

We are absolutely going to need a very careful end to end verification on the E2E flow checking everything - that still hasn't happened.

So this request is also going to give them complete control about timeouts so nothing can be thrown back.
Stephen  [9:46 PM]
OK Maxime did look eventually and confirmed Sreyas right, and not HF bug.

Now onto the status where they are highlighting that QA has real size of data in, and there isn't enough data in Dev to test anything.

Now highlighting they aren't source controlling the schema tightly and dev and qa not aligned.
[9:48 PM]Maybe because Dev is naturally ahead of QA - but seems like if that's it that they are still making quite material changes right now on Dev.  Really really need this level of actual testing.
[9:53 PM]Total 1300 conversation records in QA

"Not much" in dev - 5000 - depends on the order of DAGs run.

Dev 30,000 - used for labelling - one off queries creating set

Talking now about clearing their tables and then how to recover and run things.
Nipuna  [10:25 PM]
For the timeout values, the core methods are export_query_conversation_inputs and batch_predict  but agree if you can set it per method thats fine too. Also when initializing the package it would be ideal to pass a value to update the .cfg default timeout for all:

hf_api = humanfirst.apis.HFAPI(username,password, timeout=30) (edited) 
Stephen  [11:08 AM]
OK - that's a much better idea.  Passing an override at instantiation of the object.
[11:10 AM]OK parsing conversation

default timeout in CFG goes to 30
on instantiation there is an optional over-ride which overrides that to whatever you like as a default which is used in all functions.
Add a parameter to all the functions to override it per function.

Nipuna  [10:21 PM]
Lots of debugging Deloitte bugs whole day today but I think we solved or got to the bottom of any we were involved in. Summary:

HF ERRORS

10 min timeout error 

Cause: Pipeline ran for 16 mins exceeding the 10 min timeout in their code.
Reason: QA Vertex Key RPM was low at 70 causing QA pipelines to take longer than DEV
Status: Discovered -- Sreekar needs to update


timeout=10 error

Cause: Unknown happened once in QA in their ingest_faq_insights with 400 conversations with no clear logging on method or call that triggered.
[2024-10-24, 18:01:14 UTC] {standard_task_runner.py:110} ERROR - Failed to execute job 15748 for task ingest_faq_insights (Task failed due to: HTTPSConnectionPool(host='api.humanfirst.ai', port=443): Read timed out. (read timeout=10); 36603)

Reason: Not sure. Checked export_query_conversation timeout already over-written and batch_predict timeout already over-written. Maxime saying no other tasks in that that would read the default timeout value of 10 in that task so this is an anomaly. 
Status: One Off -- But plan to update hf-module to support more timeout definition and set the cfg value on package init.
	
HF release error

Cause: HF version release killed pipeline worker however polling for trigger status kept on going for 58 mins before the bearer token expired and DAG failed
Reason: TRIGGER_STATUS_FAILURE wasn't included in the check. It was only TRIGGER_STATUS_CANCELLED and TRIGGER_STATUS_COMPLETE hence it kept polling for 60 mins. This was in the code we provided originally as even I wasn't aware of that state.
Status: Discovered and told Maxime how to fix. Airflow DAG would fail in this scenario as an exception would be raised and retry based on Airflow logic so if happens again during release this should be a handled case.


-----------
NON HF ERRORS

timeout=600 error with BigQuery Upsert

Cause: Unknown happens on QA BQ table upsert
Reason:
Status: Maxime/Rakesh exploring to repro on dev
(edited)
4 repliesStephen  [9:50 AM]
Great summary.  Super clear thank you.

On the trigger statues - this is something that we need to get into the SDK pytests as examples and check that we ar etesting for and into the docs.
Stephen  [9:56 AM]
This is going to require getting some knowledge of the orchestratorhttps://github.com/zia-ai/backend/blob/ff59b1b5c211cadcb6a224482f7fcc4207acd593/platform/pkg/api/pipeline/orchestrator/v1alpha1/orchestrator.pb.go

TriggerStatus_TRIGGER_STATUS_UNKNOWN   TriggerStatus = 0
    TriggerStatus_TRIGGER_STATUS_PENDING   TriggerStatus = 1
    TriggerStatus_TRIGGER_STATUS_RUNNING   TriggerStatus = 2
    TriggerStatus_TRIGGER_STATUS_COMPLETED TriggerStatus = 3
    TriggerStatus_TRIGGER_STATUS_FAILED    TriggerStatus = 4
    TriggerStatus_TRIGGER_STATUS_CANCELLED TriggerStatus = 5Stephen  [10:45 AM]
@fayaz this is the code you need
fayaz  [10:45 AM]
FOund that Stephen.



Nipuna  [4:58 PM]
@Stephen
Urvashi:
hi Broadhurst, Stephen Peiris, Nipuna can we get on a 30 minute call today to review the excel shared by Business for TOP? I know Oliver from your team is updating it from his side. I have added comments from my side too. It will be best to review it together and then present to Business on Monday, to clarify what can be done for Go-Live and which ones should be tackled as a Fast Follow. Let me know what time works for you.
CC Chan, Samantha

Samantha:
to clarify, some will be done as part of this project and others will be new complex scope (e.g., churn prevention) that will need to be executed by Definity in the future if they'd like to explore that on their own2 repliesNipuna  [5:00 PM]
Edit: Responded mentioning that its EOD and that Oliver had already started work on it and can sync on Monday (edited) 
Stephen  [6:39 PM]
No the week is over.  They’ve failed to plan and schedule despite prompting.  Failed to cover it last night in the allocated slot despite us being prepared to question and leaving them a slot to raise..  Failed to respond on chat to detailed information.  Oliver and I will come round the work we’ve done jointly Monday first thing and then we can bring it together with them.  

Can you see if you can wrangle calendars to get a meeting in Monday with them and suggest they use the Tuesday evening slot to cover it with the business . We won’t be able to discuss it with the definite business on Monday.


Stephen  [9:45 AM]
@oliver been a doing a great Friday working through Sonnet model TQ! - this is my morning summary of changes so far on Intents to try and springboard into daily and the meetings later.

Added/Split
 cancellation / policy_cancelled_by_insurer
 cancellation / cancellation_warning
 cancellation / confirm_cancellation
 cancellation / questions_about_cancellation_process

Split this to two
 customer_support / login_access_issues
 customer_support / website_issues

Added
 customer_support / add_person_to_policy

Added
 policy_inquiry / letter_of_experience
 policy_inquiry / remove_person_from_policy

Refactored
 quotes / compare_with_competition
 quotes / quote_review_and_help
To
 quotes / ask_why_quote_unavailable
 quotes / assistance_with_quote
 quotes / quote_price_comparison
 quotes / request_new_quote

Refactored
 renewal / premium_increase_at_renewal
 renewal / renewal_inquiry
To
 renewal / confirm_renewal
 renewal / general_renewal_inquiry
 renewal / renew_expired_policy
 renewal / renewal_date

Intents Model
91f1 46 intents
88f1 58 intents

Need to go through and retitle intents to with Spaces and Capitals similar to other - as these are directly used in the report (rathert than a mapped tag or description property)


@Nipuna Rakesh acess woes ongoing on email it looks like - @oliver and I trying to head off the sonnet/nbs topic report issues - could you see if you can close out Rakesh access so he can raise things having looked at the data more.>

Mathilakath Rakesh
Thu, Oct 24, 6:51 PM (4 days ago)

to Sreekar, Nipuna, Zeeshan, Mark, me, Shreyas, Ehsan

Hi Sreekar,

The IAM request is complete.But just checked the HF and I do not have access still.Do u want me to wait for some more time?Stephen  [12:56 PM]
Definity call prep - here is a brief and plan for the call @dubois

The business is asking for three level of changes
- Change that can be done on the model - splits etc.
- Changes that would need substantial prompt rework to look for specific things - for instance the difference between primary and secondary drives
- Changes that would probably need new prompts entirely - was this churn avoided (retention successful/unsuccessful)

Status against first stage
Have completed updating sonnet intent/reason for additional granularity where possible and giving answers for others.
This has proceeded with then assumption that we don't update the prompt.
Will complete NBS to same standard by EOP tomorrow.
Have detailed report of before and after we can walk through

What level of changes?
Need to decide what level of update we are prepared to do
A the moment we are doing just classification model changes
Opening up the prompt opens up potentially very large rework.

How is QA going to be attempted?
Getting through QA anyway looks very challenging, as the test results haven't been aligned in the dev work (i.e whether a pass or fail has never been evalauted)
I.e there is no Topic is 84% passing number.
Data also isn't present in dev it looks like for those tests, so a clean test set would need to be a starting point to get tot that.
We can't update the prompts until we have a baseline to work from and check improvements / retardation against.
Can walk through their test spreadsheet and do examples on screen.  I think that would be very useful.

If we do start updating the prompts it is likely to raise a lot of updates which will have knock ons to DAGs and changes on the structure of the report. (edited) 
Stephen  [1:24 PM]
Shared this suggested agenda with Deloitte:
Suggested agenda for today.

Look at examples of the level of change business are asking for 
- Change that can be done on the classification model only - splits etc.
- Changes that would need substantial prmopt rework to look for specific things in it's summary - for instance the difference between primary and secondary drives
- Changes that would probably need new prompts entirely - was this churn avoided (retention successful/unsussessful)

Run through updates done on Sonnet and will complete NPS by EOP tomorrow
This has proceeded with then assumption that we don't update the prompts.

What level of changes?
Need to decide what level of update the project wants to go to.
A the moment we are doing just classification model changes
Opening up the prompt opens up potentially very large rework across multiple areas.

Discuss how QA for Topic report is being done.
Review the previous dev reports and which are accepted already as passes or fails.
Determine what the current accuracy/business acceptance level is at.
Look at the data gaps on Dev and how they might be solved.

Use this to determine how much change to attempt on the Toppic report.Stephen  [3:29 PM]
Here is the same sheet updated to have the class of change for each line item as requested.

Excluding where no change was requested then, this is the breakdown for the Sonnet Intents. Essentially 75% of requested changes are addressed by either explaining the class, or making the change (as previous post)

For topics there were only 2 Explanations so 100% of changes addressed.image.png Stephen  [4:53 PM]
@Nipuna we've got the two sheets back from Tawsif at Definity.
Oliver and I will try and sort topic can you stay on these two?
We should be a much better position to answer and respond and tweak/rerun those than on topic having drilled through making sure we had the datasets and the full evals.
I know you've got Nesto close out and Zapier investigation to start, can you let me know how we should fit in going through these as well.


Stephen  [9:16 PM]
So the expectation seems to be we now attend each client standup at 11EST, as well as the provided slot at 14:00 EST.
We're also now basically presenting the entirety of Topic report every time it comes up.
Just spent the last hour writing BQ SQL to debug their diarization.
Turns out they may have 5% of calls with no client side utterances - Sreyas raising a ticket on the project, and may ask for a feature request to show these in the views, or to raise an error or somehow so they can be found.  Explained that viewing the client side only is very fundamental to a lot of screens.   He's raising as a first a diarization fault, and second for the DAGs to exclude these.
Thank you for everyone for running round on the pipeline embedding failure.  Needless to say though Deloitte eager to jump on it as the most critical thing happening.
Still haven't done any joint E2E testing - today with Sreyas on was the closest.
Everyone in meetings discussion whether FAQ can go live with where they are up to.
That was taking priority so we had only Urvashi after 25min and no one from business on.
Nipuna doing a 1:1 with urvashi with a preview of materials tomorrow - warned that may change on Thursday
I'm going to send out the retraining materials now.


Nipuna  [9:12 PM]
Synced with Urvashi on SRA changes. Mentioned most changes were made, test results look OK but said explicitly they don't cover a lot of the new classes.

Her response was business unlikely to do another test set and will have to wait till UAT to see. Told her to make that clear to business.
To mitigate I added examples for business to review for each of the new classes so if theres anything immediate at least they can point out from their review.
Email sent with the deck, test results and comments to be shared with business.


Also stayed on for 45m with Rohan walking through how to merge changes from DEV to QA for Topic. Did the changes interactively. Although no prompt changes were made, it would be nice to have prompts in the merge session as well for a later feature request. Didn't have much time for Zapier so will continue on tomorrow. (edited) 
5 repliesNipuna  [9:13 PM]
Summary from email:


Callback Report
- Only change requested was to add None (which already exists so no change was made)

Escalation Report NBS
- 5 Classes were requested to be added and all 5 were added
- 1 Class was requested to be renamed and was renamed (Underwriting Clarification to Underwriting Support)
- 1 Seperate Class had to be renamed to avoid confusion with an added class (Documentation & Process Unclear -> Documentation Unclear)
- NOTE: Although the results are looking grounded, the original test set doesn't cover these new classes in detail so there are examples in the deck to verify. Until UAT or a separate test set is completed, we cannot verify the full validity that these classes are matching as intended.

Escalation Report Sonnet Support
- 5 Classes were requested to be added, only 3 were added. 
- One was a duplicate class that already exists (Policy Inquiry is same as Policy Clarification and was not added to reduce confusion). 
- The other class, "Quote" was not added as it requires more explanation as to what it means in the context of an escalation reason.
- Same situation here with the testing data only covering a limited amount of the new classes added. Please review the examples in the deck and the testing spreadsheet.

Escalation Report Sonnet Escalations
- 3 Classes were requested to be added, only 1 (Billing Inquiry) was added.
- The class "None" already exists in the taxonomy so was skipped.
- The class "Premium" was not added as it requires more explanation as to what it means in the context of an escalation reason.
- Please review the examples in the deck and the testing spreadsheet.

The deck contains examples for each of the new classes, for each of the prompts for business to review. The business excel with comments is attached as file (Modded_Escalations Report Categories.xlsx). The full re-run test set across all 3 prompts is also attached (Escalation_Report_Rebaseline_Oct28.xlsx) with the results.Stephen  [1:44 PM]
Great thank you @Nipuna - gone through the email.  Great deck.

I'm going to use this as an example at 11 EST against the presentation of Topic of where it's so important to have the test set baseline to make these sort of changes specifically.

To support that could you do another SRA single slide which summarises the data from slide 8/20/29 along side their previous results (Couldn't see here)

So for each report in a standardised way so you can read across them on 1 slide, previous result, current result.  Against Fail, Maybe, New Cat Valid (obviously none previously), Pass, and then the aggregated green/red headline figures.

and a second one which just has the callback result to match it, i.e previous result in same format, no changes.

These were my top level summary of changes.

Callback
1 explanation no changes - no retest needed.

SRA - NBS
Prompt update - 1 rename, 4 new positive classes, 1 new "None" negative class.
Slide 8 76% headline figure -  previous?

SRA - Sonnet - Support
Prompt update - 3 positive classes added
Slide 20 - 79% headline - previous?

SRA - Sonnet - Escalation
Prompt update - 1 new positive class
Slide 26/29 - 89% headline - previous? (edited) 
Nipuna  [2:12 PM]
Ok added in Slide 34/35 wondering if thats the layout?
3 files image.pngPNGimage.pngPNGDefinity-Review-UpdatesGoogle SlideStephen  [2:20 PM]
The alignment makes me twitch ; -) But yep that has the key information on TQ!

Callback
1 explanation no changes - no retest needed.
NBS - 82%
Sonnet - 84%

SRA - NBS Escalation/Support 
Prompt update - 1 rename, 4 new positive classes, 1 new "None" negative class.
76% headline figure (73 previous) +3%

SRA - Sonnet - Support
Prompt update - 3 positive classes added
79% headline (85 previous) -6%

SRA - Sonnet - Escalation
Prompt update - 1 new positive class
Slide 26/29 - 89% headline (89 previous) +/- 0%Nipuna  [2:25 PM]
Yeah sorry on the alignment haha (different resolutions of screenshots from different decks). Tried to fix a bitimage.png


Stephen  [9:25 AM]
So there is a thread on FAQ keys - adding here so can help track. Friday 17:45

  The background here is that a) they are trying to go live with FAQ and b) they have a lot of calls which aren't processable (probabaly 3-5% of data) because either

 the diarization has produced a number of roles IVR SYSTEM AGENT - which map to expert, and no roles CUSTOMER (UNKNOWN - in some cases this may map to agent - it's buried in the DAGs) - so there are only expert utterances or
there is only one conversation utterance on the expert side so it's too short and ends up with the above
So they are trying to work out various "None" no situations.
Definity are worried that they can't understand the numbers in the different failure cases.
Deloitte are trying to manage them to get off site.



Gelinas, Maxime01/11/2024, 13:42Peiris, Nipuna QQ, currently we return no predictions when no faq are found. this make it hard to monitor since we dont know if its an actual error or a legitimate no faq case. how much work would it be to return null is that case?
So the prompt is currently outputting an arbitrary amount of keys in sets of 3 (question, reasoning, snippet) for the questions it generated. If a conversation_id in the pipeline export doesn't have the key "question" then it didn't have a generated question and the pivot df will probably exclude that id. You can probably find those by comparing which convo_ids are in the original pipeline export that are not in the pivoted df via code. Those IDs actually were likely processed but didn't have a FAQ generated. There is an exception case here which is it could have been an LLM error (error metadata key would exist) so it didn't get a prediction due to VertexAI. 

However, if there was an conversation ID in the original BQ export JSON but it wasn't in the pipeline download, then its likely that conversation wasn't read by HF. Meaning it could be a case where there's only agent utterances (Shreyas was mentioning this is actually around 3-5% of the data). So the reason it didn't get a prediction was b/c it wasn't run as it didn't meet the requirements.

We can attempt to change the prompt to say None if no questions were found but given FAQ is so close to PROD release, making this change now after all the testing and verification is done seems like wrong choice. Can you verify with the code approach of comparing the two df's and logging the convo_id differences?(edited)
Stephen  [11:27 AM]
@dubois is there a moment to do a debrief on the Deloitte call yesterday?

they've asked again for us to do the changes we said we couldn't do without a baseline test being established - this seems to be after the meeting slot you had yesterday and ignores all previous meetings and correspondences we've had.  If we are to take on this topic reports, then it needs to be part of a frank discussion with the Definity/Deloitte that the rework will be significant, and may involve DAG changes and who will then do.  So at the moment, I have repeated that we can't until that test is complete and asked for progress.
We've got the weekend work which has run into difficulty with the DAGs and Nipuna, me and Matt trying to help debug.  It isn't clear yet from what I can see where the issue lies (might be us, might DAGs, might be saving the CSVs somewhere, might be difficult call)  - though Sam clearly escalating it as a HF issue which provides her something to point at.
Stephen  [2:49 PM]
Converted the Definity deck to be a generic one and build supporting ABCD materials.
Added all the steps here - posting here because it shows quite how hard the flow is even when you keep the focus on the model really tight.


Stephen  [10:11 PM]
Discussion on reordering reports - callback depends on topic so that can't
Basically Urvashi pointing out that Definity testing takes for ever to get going at everything and they are focused on Topic nowe and don't want them to lose focus.
So whilst SRE might eb abel to swap round in her opinion not worth the socailisatin gand comms - which is reasonbale.Stephen  [10:29 PM]
On BTS - Urvaashi wants to estimate with Rohan how many BTS calls present in the training set used to build the models.
However which exact pipeline runs were used and which prompt versions, really not clear.  The data left on the environment very messy.
As we haven't attached detacted anything - I've downloaded the files for her and Rohan so they can make some estimate.
She has 6 skill groups that make up BTS calls.Stephen  [2:41 PM]
hi Broadhurst, Stephen Definity is now aligned on getting a baseline for TOP first, then start the activity of adding more sub-topics for 'system support' for NBS. The ask now, is to get an estimate of the work required to add these sub-topics. This estimation will help us in proposing new timelines. Could you give me a rough estimate in a few hours please?
CC Peiris, Nipuna Chan, Samantha
 That won't be possible to start that estimating until the baseline in place.

Once that happens there will be an indication of the gap needed to be closed.
Based on that the project can then conduct a full review of the prompts in place, any new requirements, and make a recommendation of the steps necessary to fix.
Each team can then make an estimate of the necessary changes to implement that.
This itself might take a week or so given the state of maintence of the dev environment, and requiring to bring on new resources to replace the original ones who were familiar with how exactly those prompts and models were constructed.

To give an idea of the range of uncertainty we face until that baseline is established.

If the baseline meets business needs and there are no new requirements then zero duration for rework is required and topic can go live.

But for instance, If a full rebuild of the prompts is necessary including splitting intent and reasons into two workspaces/pipelines and the resultant and DAGs updates.  This might for instance be 4 weeks work duration across the teams (subject to those teams making their individual estimates and having resource availability)

My guess is that given the new requirements look quite extensive, the language changes requested to the prompt classes and the areas theat prompts is being asked looking for across both intents and topic are also signifcant: That there is a high chance of a major rework being needed and that once that starts the probability of the topic and intent changes conflicting is likely, therefore probably necessitating splitting out topic/intent workspaces and pipelines to achieve good results.dubois  [2:54 PM]
I spoke to Anand yesterday and we’re aligned that no additional work will be done on Topic model until we’ve released a first version, if they require changes to the prompt etc. we will scope out a paid for Phase 2
Nipuna  [4:46 PM]
Sam has booked in a call today for 1pm EST I guess to discuss the BTS call details. I have a conflict with the other Definity Team KT session. @Stephen I can try to push KT for next week? CC @John
Nipuna  [8:08 PM]
Request if possible from Ehsan Definity AA to be more involved with topic model (if there are changes needed to Topic model) to learn the process with a real example.
Mentioned we're still waiting on baseline, and then once plan together, we can loop them. Also mentioned Tue/Thu sessions are great place to join to see these as they go on. Ehsan requested aamir.khan@definity.com to be added to 3pm's. (edited) 
Stephen  [8:31 PM]
BTC explainer - will thread.
HI - I pressume this is for BTS Calls.
 Apologies that we cannot make the suggested 13:00 EST / 18:00 call - we are already delivering the Definity handover in that slot, I also have to cook my children dinnner, before being on the 15:00 EST / 20:00 Call.
 We have done all the changes that were possible without updating the prompts and presented in detail examples of why it isn't possible to update the other classes.   Happy to put some time in at the usual slot to go back through the existing examples why prompt changes will be necassary.
 Would it be helpful to start the usual slot 30 minutes early to recap the previous presentation on the different types of changes necessary for different requested updates?Stephen  [9:32 PM]
@mathieu @appaquet would one or both of you please be able to join the Definity call on Tuesday 15:00 EST?
Aim is post GC release to see and understand across everyone the end to end process - flowing through the DAGs, their logs, and then seeing the pipeline running in GUI
Discuss the timeouts and retry and durations involved and files so we have a really good end to end understanding in case there are issues when they go for the big volume.


Stephen  [11:32 AM]
A lot of ground last night, there are a lot of inter related issues which we'll also get documented and plans for. But to de-noise, this (still long) post aims to just cover the central issue and the immediately available actions to unblock testing.

This is probably familiar to people as the "retries" issue, but to explain what is causing those retries.

Typical client approach with HumanFirst is
Overnight batches bringing new data into the tool
Maintaining a controlled "rolling window" of active data in HumanFirst to investigate results and track model drift - by deleting old data once new data is uploaded.
Data is then available through the day to do various processing and export of insight for follow on analytics (where it is stored for long term in a data lake)
Data volumes at these clients can be very large (much bigger than here)
Typically there is one file per day.
The rolling window manages a relatively small number of total files.
As the individual batches are large, therefore whilst the import processing time or pipeline time is significant, the index update time is also significant, the number of index updates per day is small
So whilst the individual index update takes some significant time overnight, the percentage of days total processing effort used small.
Typically the number of turns in a conversation is medium, 10-30 turns is common.
Typically each turn is roughly a sentence or two. (Chats, sales calls, bots, etc)

HumanFirst supports cross file conversation utterance merge which helps these sort of clients.
What this is if you have say a chat conversation which starts at 23:00 and ends at 01:00 it will potentially be split across two files
When each file is imported the IDs are checked across all files in the conversations set, and all the utterances for a conversation indexed against the conversation.
What this means that when the first day is in you see the chat up to midnight, and when the second day is in you see the full conversation
This means all the clustering, organisation, and inspection works for that conversation despite it bridging two files.

At Definity the approach is currently:
There is a large backlog of data to be processed (the catchup ingestion of calls - this was what was under test last night)
To have near realtime updates of dashboards the frequency of import to HF is tied to pipeline runs and is ~30mins envisaged currently
Each batch size is relatively small to fit into that processing window at 400 records per file
There is not yet any management of that "rolling window" i.e deleting old processed files - so the number of files quickly grows to be large in testing.
That same process envisaged for day to day running is being asked to process a large backlog which means that there is the desire to run a lot of batches in quick succession to catch up

What we observed last night is:
The DAGs are batching entire conversations per file (cross file merge in HF not required - we are thinking whether this helps in someway)
Because the frequency of file addition is high there a lot of index updates.
Because there is no rolling window inplace, the number of files quickly grows to be very high.
The conversations appear to often be very long (project should establish metrics but often we see > 100 turns)
Sometimes they have very long utterances (again project should establish some metrics - but browsing we regularly see almost a page of data in a single utterance)
Currently in QA we saw 51 files 400 convos each in QA, 20,400 conversations across chat and calls, 2,600 estimated per day.
The net affect is that the indexing process has a lot of work to do when it runs - long conversations with many large turns which may be split over many files .
and it's being called very often.
Hence index processing is starting to eat up a large proportion of the days processing effort and getting in the way of multiple other tasks in both the GUI and the API.

Examples are
For many tasks it is necessary to download the index internally in HF to perform actions.
If it is not present either the task must wait, or it falls back to the previous index version.
This leads to some of the other knock on symptoms like not immediately being able to see the data in file once it's uploaded, or the GUI showing a blank data screen until the data was there
The index was currently 10GB last night which is very large compared to what we normally see.
When this causes jobs to retry, this can potentially compound the problem.

Immediate actions recommended (most already started)
1. Implement the rolling window to manage the number of files down. (planned next sprint)
Initially this was envisaged as based on a configurable 90day window managed by the upload to humanfirst DAG
That looks too large with the shape of the data being operated on.
That was also based on the previous file naming assumption which was that files are named per period they cover.
For a variety of reasons around catch up/long running calls that's not the case any more here, we saw that files are named by processing isodatetime_numbercalls.json
Recommendation is to simplify and accelerate this implementation by changing that from a number of days to just a number of files
That will keep it onto one page and save maintenance scrolling, and tie the number directly to the driver of work (files rather than days)
Recommend a number of 10 right now, that is 1/5 current on QA and equates to about 4 days load.  
That will give about 4,000 calls which is enough to work with in the tool for necessary model maintenance.
As things develop this can be tuned to balance data visibility and performance.

2. Implement a configurable delay before attempting to download the data from the pipeline to reduce retries. (Already developed needs deploy to QA)
We saw lastnight the problem potentially compounds when retries are starting on top of each other whilst the indexes download
Currently we see after file pipeline completes the DAG immediately try to download the information.
This change is to put a configurable wait before the first attempt is made to allow the index to be ready to allow the first attempt a chance to succeed.
If the number of files is managed to 10 as above, I suggest this is currently put at 120s.
Again we can then look to tune as things develop.

⁠Gelinas, Maxime what are your thoughts on moving to a number of files rather than number of days for rolling window? 

In terms of effects on the release of ingestion release.
The ingestion release will start building the backlog to come in.
As no report/insight DAGs are planned to release this doesn't affect that release.
But the release will start building the backlog in prod, that we are then seeing in QA and testing.
Above changes should allow to unblock QA to allow the current batching strategy to be tested without regular retries.
Further actions can then be considered.Stephen  [1:13 PM]
Mishra, Urvashi
Thu, Nov 14, 8:08 PM (16 hours ago)
to Steven, me, nipuna@humanfirst.ai, Samantha, Rohan, Maxime, Ramkumar

Hey Stephen,

Attaching the updated UAT results from Rakesh for Topic Modeling report for Sonnet. NBS is still in progress.

Regards,
Urvashi

Surprised it's so high Urvashis previous forwards (See PNG)

The TOP baseline is still in progress, and we expect to see the results tomorrow morning. For Sonnet, we're heard the accuracy is around 50-60%, so the Business team is dedicating extra time to ensure the calls have been analyzed correctly. We haven’t received any updates for NBS yet.


Contact reason is blank for 36% of calls
Accuracy of Contact Reasons is ~ 50%
Accuracy of topics/sub-topics is also ~ 50%


Stephen  [4:28 PM]
Had a meeting with the Deloitte at their short term request to help them understand

implementing the rolling window and delay after pipeline finish asap to let testing proceed - we provided code hints and examples.
the issues with the QA run and the data quality for TOPIC INTENT/REASON  - and how we are gathering a test set together that can be updated and start to be iterated on.
their major question is how their data catchup is going to work - that's very unclear - using the same method for hour by hour runs and to bootstrap a large amount of historical data is possibly not thge best way to accomplish this.
there were some questions like - why did we only find this out last week, and the answer to that is the agreed E2E testing we had talked about for months only happened for the first time last week.
a second reason is that they never consulted with us on how things like that should work, just assuming that their design would work against an untested system.
Maxime made some excellent points about testing with the new rolling window and delay.
ask is to think about what we can do.
To help them design a better catchup.
Or raise the system limits on rolling window to use their existing approach 
some other answer.

@mathieu @appaquet can you spare some time 13:00, 14:00 or 15:00 EST to talk about Definity?
Deloitte are concerned - I'm trying to keep them ontrack doing useful things, but we need to plan out what we feel we can do (or not do) more going forward.  These are the sort of questions I have.

Why is the index so big?
- shape of calls?
- is there an issue inflating the index?
- is it one index across file upload and pipeline run - i.e data/unlabelled and generated?

Why does index processing take so long?
- is the conversation merge across file the key here (feels like it may be) Conv Size x number Files x Big utterances
- can we make that switchable at the convoset level to have a more file by file processing?

Do we need all the data in the current index?
- for just pipeline results do we need everyting - could there be some sort of "no-interactive-mode" that has trimmed down results either for batch load or for every day runnign.

How is a better way to get a big set of catch up data into the system
- Many small batches mean many index updates.  1 big batch means one.

Then just to have somewhere to catch them - as well as the major performance/workflow things above.
Tweaks to make it better on that route.

GUI
When index is downloading get a variety of issue
- blank screen - takes
- spinner
- no ability to find just uploaded/created

Can we tell them better by API when index is available
- Tickets raised12 repliesmathieu  [5:38 PM]
we were just talking about it this morning. I think the problem is not the size of the index itself but the fact that we're not giving much feedback, and that they have to poll until they see some data from their query

if they're talking about post-trigger-completion-delay then it's purely a network-bound issue due to how we persist things in google cloud storage

Frontend bugs will be raised for the lack of refresh after download completion
appaquet  [5:53 PM]
Already done: https://zia-ai.atlassian.net/browse/PB-8110
PB-8110 Fix large data set query readiness logicStatus: TODOType: BugAssignee: Sebastien DanielPriority: Medium:information_source: New: Click Notify to receive real-time issue updates directly in this channel.Added by Jira Cloud[5:54 PM]@seb did we have one ticket for indicating that you are currently seeing old results because the new index is being downloaded?
seb  [5:57 PM]
Nope
I take it the best solution would be to show a header of the index being made ready and explaining that we;re currently showing outdated data?appaquet  [5:59 PM]
Yeah
Stephen  [5:59 PM]
I think the problem is not the size of the index itself but the fact that we're not giving much feedback,

More info is useful - but right now with ~50 files ~ 6days the end to end workflow is too long to run in their 30minute window.

They are demanding (rightly or wrongly) 30days minimum (they want 90 days) - so 250 files right now my prediction is everything would grind to a halt with that sort of volume

Telling them to get down to 10 files, with a 120s delay to get Rakesh testing reliably in SIT from a functional standpoint - but they'll want to know what our upper limit to that practically is, and what the time will be to wait on each end to end file processing. (edited) 
mathieu  [6:06 PM]
where does the 30 min requirement come from?
Stephen  [6:09 PM]
So their daily schedule is a dashboard update every 30minutes (it's been 15minutes and 60 minutes whilst I've been here) but some number nearer to hourly rather than daily.
That in production will be less than 400 calls, when they are caught up.
Because they are behind, they've promised a data catchup from June sometime, and their plan is to reuse the daily production running process as hard as possible (i.e 400 calls per 30minutes) until they catch up with now and then start keeping dashboards up to date.[6:13 PM]Hard to explain via text is there any time for us to talk @mathieu @appaquet?
mathieu  [6:19 PM]
we're free after the sprint kickoff at 14:00 EST / 19:00Z
Stephen  [6:19 PM]
Cool
appaquet  [9:36 PM]
@seb coming back to this one. did you create the ticket for showing when you don’t have the latest index? we may have to change the behaviour of how we download indices behind the scene to prevent massive workspaces like the ones in definity from impacting the rest of the customers, and showing the user will probably be even more important. Right now, as soon as a workspace index is ready, we download it on the search services, even if no-one is asking for it. This has been there for a while, but we may have to remove that (I’ll put it behind a config so that we can revert if that causes an issue), but in the case of definity, every single time they upload a new file to the dataset, since it’s linked to 8 workspaces with ~10GB index each, it results in ~80GB to download on the search daemons on every file upload, even if they aren’t even querying them. (edited)



Nipuna  [11:19 PM]
Here's where I'm up to with Sonnet: Got around 44 predictions labelled, spent mostly focus on the intent section. Tried to label things into MISSING/PRESENT in csv and CORRECT/INCORRECT with a likely problem.

Got around 44 results from 11/51 call ids labelled. Right now if you include the Ambig cases (which are mostly leaning correct) its around 75% correct to 25% incorrect. Around ~42% of intents/reason pairs generated are MISSING so not in the original Rakesh spreadsheet.

Generally I think the classification model needs work (things marked TRAINING_GAP are where the classification is not predicting correct). It is looking like few new intents or seperation needs to happen, but unknown yet if the prompt produces enough granularity to not cause confusion. Need to verify this tomm with the pipeline data we have available across QA/DEV. Majority of the time the core call topic/reason are identified. However prompt generally seems to provide too many “intents” per call with no ordering of significance. Overall though the newer results from latest DEV model look better than the old trained model. Attached the spreadsheet so far. (edited)


Model review questions answered

Shreyas Ragavan Tue, Nov 19, 10:15 PM (11 hours ago)
to me, nipuna@humanfirst.ai

Hi Stephen and Nipuna,

I would be grateful for your advice on the following questions regarding the HumanFirst NLU. You mentioned that it was based on the Google Universal Sentence Encoder (USE). I see this is described in a paper and available open source https://arxiv.org/abs/1803.11175. 
 
Could you please help me understand how the HumanFirst NLU is different from USE? (Please do feel free to share any reports or pointers to documentation.)             
Is the core of the HumanFirst NLU encoding model updated at some cadence?
Is my assumption correct that the NLU model version we select in our workspaces is not automatically affected by any such update?

Has the HumanFirst NLU undergone any kind of technical peer review by a party independent of HumanFirst?
 
Please let me know if any question is unclear, and I look forward to hearing from you. For context, I would consolidate your answers into the ongoing model risk assessment.

My answers

Stephen Broadhurst <stephen@humanfirst.ai>
9:55 AM (0 minutes ago) to Shreyas, nipuna@humanfirst.ai

Hello Shreyas

Of course, let me work through them here, and also happy to spend some time explaining if you would like.

> Could you please help me understand how the HumanFirst NLU is different from USE? (Please do feel free to share any reports or pointers to documentation.)       
USE ( https://arxiv.org/abs/1803.11175 )  is an embedding model - it encodes sentences into embeddings (vectors). These can then be used as features in your NLP machine learning approach of choice.
As such it isn't any form of NLU on it's own, you need to use it with a specific objective in mind - for instance intent classification.
HF NLU is a perceptron based (https://en.wikipedia.org/wiki/Perceptron) intent classifier, it by default uses USE embeddings but can use any sentence level embeddings of the client's choice.
It's an example trained classifier, I.e you provide examples of the classes (ground truth), and it trains a model to take any future utterance of similar shape and size, and give you a "confidence" level, of which class it feels the new utterance is most similar to based on the ground truth examples it has.
It is not auto trained, rather training is manually triggered via the "Train NLU button". At that time it takes all the ground truth and provides a training exercise, running through multiple epochs where it shuffles the data into training sets and performing training trying to iterate on the results to achieve matching the most of each class training to the class, whilst minimising the number of utterances not in a class mistakenly matching the class.
After it is trained the model weights are saved as the "model" and deployed to the workspace and can be selected from the drop down in the tester.
It can then be used to make all the other predictions in the workspace.

> Is the core of the HumanFirst NLU encoding model updated at some cadence?
There is no automated or regular process for updating the encoding model. 
We support others embedding models for instance MiniLM-L6 and L12 are popular with some clients, especially if they have more paragraph style than utterance data.  
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 
https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2
As such then a client can chose any appropriate sentence transformer based model and model version they use.
I haven't seen us take an update to USE since I've been here, but as USE was first introduced in 2018, there are more advanced models we have been evaluating.
Currently we haven't switched the default, and even if we did we would I expect make it an option to select a particular set of embeddings like USE so clients didn't have to see a change unless they wanted to.

> a. Is my assumption correct that the NLU model version we select in our workspaces is not automatically affected by any such update?
Yes once the model has been trained and the weights fixed, that remains fixed and unchanging until such time the train NLU button is pressed again.

> Has the HumanFirst NLU undergone any kind of technical peer review by a party independent of HumanFirst?
Perceptron classifiers and sentence level embedding models have been thoroughly peer reviewed. We implement typical examples of the types.
We are fully SOC2 inspected each year and have made the report available, this includes detailed evaluations of our technical systems.
Many of our clients compare in detail the performance of it with one of the external NLUs we support like DialgoFlow or RASA
In such tests it can be seen to give very representative results of this sort of example based classifier and the HF NLU system normally outperform these systems on a number of test sets.
If you wish to conduct such, you can setup a DialogFlow instance in your GCP and we can show you how to export one of your models to DialogFlow (this has full in tool support) and run back to back tests on HF NLU v DF for both K-Fold and if you establish one any blindset.



Let me know if any other questions, and if you want to book some time on this topic you can use this link to see my calendar and grab a slot
https://www.getclockwise.com/c/stephen-humanfirst-ai/shreyas-model-review

Sincerely

Stephen


Nipuna  [4:52 PM]
Hi John and Nipuna,

Thank you for completing the KT series with the team.
If you recall during one of the sessions we discussed the possibility of AA members learn from the latest topic modeling changes that is happening based on business topic changes. I was wondering if the work has already started and if there is still the opportunity for AA members to join you during some of these working sessions to better understand how this type of changes takes place in our solution?
This can help us greatly getting prepared for similar scenarios.

Thank you,
Ehsan@Stephen @oliver The Definity AA team requested in our previous KTs they wanted to be involved with the topic model fixes going on to understand the process. We were just getting our heads wrapped around what was wrong so can do this but it will slow topic model fixes progress having to explain how to do something complicated while doing it. Maybe a solution I can propose will be like a 30m sync EOW to explain how we made changes / thought process now that 3pm's won't have Definity?
4 repliesStephen  [5:20 PM]
We need to be coy on this until the Topic replan is worked out with Definity

And not offer any time..   more detail following.
[5:21 PM]Urvashi here positioning in teams
On a separate note Broadhurst, Stephen I suggest we don't bring up the estimation of time required for TOP rework with the client yet. Let's regroup on the estimates and then inform them once we're internally aligned.[5:23 PM]What's going to happen is tonight we'll do a presentation of NPS numbers, i.e what they tested, what it actually is with all the data, and the new model already delivered, then what they might get to without updating the prompt, then leaving what might happen if updating the prompt.

There is a discussion then about who does it.

I presume given last nights shennigans from Deloitte is that they are aiming to make no functional changes at all, it's all handed over, they just have to do the batch and get out.

Hence what Shreyas is probably actually asking is

"we've agreed with deloitte I have to make the changes"

"but I'm hoping I can make you do them and I watch"

So we can't offer to sit in on model changes, because there aren't any model changes committed to.
Nipuna  [5:26 PM]
Ok noted thank you for the detail. Will politely decline saying no topic work ongoing at the moment until further discussions with Deloitte on baseline results.


Stephen  5:59 PM
NBS Testing write up

NBS Baseline had 42 calls in it, one of which we couldn't locate in the provided datasets on HF to examine
The baseline used two annotators we've consolidated into a single tab and noted the annotator.  The annotators didn't overlap on any calls so have not tried to investigate alignment and carried their comments forward verbatim.
The baseline as provided was 24/41 (59%)
Examining it, it was clear it was missing a lot of data that is present in HF for instance where multiple classes had been predicted not all of those were on the Baseline.  Sometimes those extra categories already satisfied the Agents comment.  Adding that data in brought the result to 40/67 (61%)
The baseline was run on QA with October 1st model without the updates that were made on Dev.  Re-running the test call set of dev and aligning the original agent comments against the current model gives 43/67 64%

Examining the remainder
We believe that there are 4-8 additional that can be improved with model only changes, which would give between 70-75% on the baseline.
Any others would need prompt changes to improve the granularity of data to classify.

Example call to talk about from the testset here @oliver if possible before call.


Stephen  [12:19 PM]
@Nipuna @dubois we're seeing now a lot of more formal emails from Deloitte to HumanFirst accounts.
We're in the situation where we are having direct meetings with Definity and they are setup on our systems.
We see Deloitte actively trying to hand off work to Definity and us.
I think the fact we have Deloitte emails is a confusion and that teams is not helpful.
We're logging things there, and having to duplicate in slack.
Deloitte are raising things there, they are documented there, then they renege or reunderstand them to their convenience later.
They delete the history after a month.
It's a high load on me and Nipuna to have two laptops/two browsers and two places to check for things.
My view is that we are getting very low value from this.
Definity create things that we can't access even with the deloitte access in confluence.

I would propose that we hand back the Deloitte kit and access, and work just within the core HumanFirst tools with Deloitte and Definity in the most professional manner possible.

What are your thoughts?
Stephen  [6:23 PM]
@dubois @Nipuna checked with Matthieu he agrees and explained the Desjardin experience with laptops - sounded horrible.  Same at Bayer. Let’s not do it ever again. I am going to write to Deloitte and explain and delete all their things.  

Nipuna you’ll need to ship the laptop back to them. 

Speak now or forever hold peace!
Nipuna  [11:05 PM]
Sonnet model EOW status

Sheet manual rebaselined up to Agent3 call_ids (85 / 120 predictions) on the latest model in DEV
Around a 73% correct (incl. ambig) / 23% incorrect 
if you ignore any predictions below 0.3, then it goes to ~75% which seems to be what Rakesh was seeing when they were doing testing

Think we can get a pretty decent bump in total correct with some classification model intent additions / fixes (noted some in screenshot)
Started some initial testing and adding around separating out Quotes
In a test workspace gathered all the prompt outputs and got from 58 intents originally to 70 but haven't re-baselined anything yet

The prompt not outputting enough granularity is a problem but for Sonnet I think the classification model fixes will help since not much granularity is expected unlike NBS. Prompt can describe a key issue in multiple ways run over run.
Not sure if its worth doing the rest of the sheet as the problems are clear and its quite time consuming
(edited)
3 files image.pngPNGimage.pngPNGSONNET_EVAL.xlsxExcel SpreadsheetStephen  [5:34 PM]
Hi Chan, Samantha Mishra, Urvashi same will come by email, but a quick update on our Deloitte logins.

Could you please contact Deloitte IT and have them revoked, along with the VDI and let us know the address to return Nipuna's laptop to.

Whilst it seemed at the start it should be useful, it's actually turned out not to be.   We don't get access via them to any Definity project materials, we have a lot of extra overhead dealing with the segregated machines, they are very locked down (to the extent to not be not useful at all), and the Deloitte addresses it creates a lot of confusion 

Most communications already now coming direct to humanfirst.ai addresses thank you, and we're getting the sessions setup for Topic and Batch loading etc.   So we are going to be doubling down on this.

This will be my last post here, looking forward to talking to you in other forums shortly.[5:34 PM]Mathilakath Rakesh Shreyas Ragavan we've got you setup on the portal, you've got our emails and we have the dedicated handover sessions going. We'll have the next test coming up shortly, and workthroughs on Sonnet and NBS Topic.

We've tested out that if we want to work on a doc together HF and Definity it's easy enough to share by sharepoint.

As such we're discontinuing the Deloitte emails, which are difficult as it's a separate machine to check, file access is very limited, there are a lot of logouts, it creates a lot of confusion for people and doesn't actually give any access to project materials, like confluence.

As such this will be my last post here. Talk to you soon in other forums!Stephen  [9:57 AM]
Decommission Density?
@seb @mathieu @appaquet
This came up across NLU/PxD split and Definity conversations and wanted to come to a plan one way or another with it.

Background 
Matt found that Density calculations scale quadratically not linearly with dataset size - so trimming them would save a lot of processing on big data sets.
Density as a concept never really made it out of a "see if it's useful" phase.  The net of that was you did get a slightly better uncovered intent discovery process if you used Density + Uncertainty but it wasn't a big difference and it needed more clicks to make it work.
We released a shortcut for uncovered data view to try and make that easier, but it never got beyond one view. (See SS)
There is a section in the docs here
https://docs.humanfirst.ai/docs/workflows/discovering-new-intents/#discovering-intents-with-density

Options:

Keep and tune?
Hard decommission - remove the calc everywhere, the docs and the feature

Maximum load saving, reduce maintainability load, get some screen space back from the control not needed any more.
People can just rely on uncertainty as their core metric.
Maybe some people miss it - can we tell in MixPanel - but we can say it was experimental and turned out to be too much load for too little use.

Soft decommission - switch it off, only turn it back on if someone asks

A way to find out if anyone really uses
means we have to maintain the knowledge about.

OK Great work @oliver @Nipuna I've consolidated it into this deck along with the test environment, my work and a worked example.

@dubois @greg as Definity has a large impact on time have a quick look at slides 2 (what we can achieve ~ this week), 3 in particular  (which limits what we intend to do for them functionally going forward) and 5 (which has the core environment where we will have to test and do multiple fixes to meet the performance requirements - which will be extensive regardless of the functional work done or not with them).
https://docs.google.com/presentation/d/1cvd5NCdy_q6fZFu-yNgLjK2tFO5YLFSabgFrF9ilL8Q/edit?usp=sharing

The worked example 7-16 is interesting if you have the time - it shows how very small prompt changes can have very large impacts on the ability to show things in the end reports, and how important then rapid evaluation of different prompts against a baseline is.Google Slides


Stephen  [7:50 PM]
Agenda

See who comes - may well be we have Definity
Walk through Topic model analysis from last week - TL:DR slide 1 page walk through.
Explain they should have those in Dev by end of week
Check they know where to find Beamer and last weeks Lazy index fixes
Show them the short cut XLSX summary of their QA environment and how we recommend they do one for each - already on email.
Show nice and tidy QA environment Multidim we have and how representative data
Play forward this weeks 1.65.1 - maybe talk about no_trigger TBD
Recap their portal requests
https://zia-ai.atlassian.net/servicedesk/customer/portal/1
https://zia-ai.atlassian.net/jira/servicedesk/projects/HC/queues/custom/4/HC-147

Talk about how supporting them over these next releases using that environment - this enables us not to have to be in their environment at all.
Check Shreyas has the sessions he needs booked in to ramp his team up.
Explain how the changes to Topic models this week will be the last functional work we conduct.
Check when they are planning rolling window tests and get that booked in.
Let them explain why the ingestion DAGs - unrelated to HF are still not running 
Let them start to work out for themselves who then that means will need to be making changes.
Recap on that no circumstances will be using their Deloitte logins.
If they talk about us "withdrawing"
point out extra help providing
point out we weren't the party rolling the two trained resources off the project.  

Having done that and having definity having accepted that handover to Definity - what is their plan?
They may want more handover and training for the Definity team - which is fine.  We can run the Definity team through and those sessions on going.


Deck


Stephen  [7:20 AM]
Morning @oliver and @Nipuna we had a somewhat confusing call last night on batch loading and performance which I'm going to try and focus on straightening out today.
We did present the above, and it was very well received, but not the expected focus of the meeting in the end.
The net net on Sonnet and NBS Topic is.

We'll present to the business Topic now next week
We've committed to what is in the one pager (and already here internally on slack) is in Dev ready to go by EOP Friday.


So boiling down what that means.

@oliver what discussed yesterday in doing the final work to get to 70-75 and check if there is anything we can do to hit the top of that range or above.
It looks like do need to put down other things today and make sure that we've got there and it's all ready to go

@Nipuna I think you've already done most of the work in a separate workspace but can  you put it all in the Dev environment and make sure it's all ready to go.

I think I'm going to be very tied up with this performance stuff.
Would it be possible for you two to do some 1:1 time and peer review the two sets of work and check everything looks ship shape and Bristol fashion?

These are the things knocking about in my head that I'd welcome you putting your heads together on.
The Sonnet number seems very high - like worryingly high - the number of intents grew from 58-81 - but didn't we grow the intents already recently?  There isn't any double counting is there?
If we can get more on NPS by adding some intents that's great, but we need not to knock the model off.  It feels like the NBS calls are just harder and more complicated is that right?Stephen  [7:41 AM]
Confused what happened this last week with Definity - trying to document it here and we can circle back on.
@mathieu @dubois @appaquet

Last week we had an agreed position with Deloitte where
- they were going to implement the rolling window
- they'd always committed (for months) to actively manage the amount of data in
- they'd had in plan to implement this already in this sprint
_ the no_trigger fixes in staging made a big difference on how this would work and that could have hit 1.65.1 probably
- this was tough medicine for everyone but would work and get them live and the client off their back.
- it would actively manage the amount of data without Definity manual interaction
- we could up the amount of data in the rolling window with the planned set of fixes and had a plan for those over 4 weeks.
- we could work out how to help them batch load the data right.

Somehow there seem to be a lot of agreements I've not been privy to and now the situation seems to be.
- they are not going to implement the rolling window
- they have an await_next_index change to post pipeline data download which it's not clear they are going to manage to implement or how it helps
	- I'm going to try and close that gap today - get some stats for what it does or doesn't do, build an example - try and make it easy for them.
        _ it's not clear they've even moved to SDK2.0.0 so TBD whether if I do an example this morning and SDK2.0.1 whether they'll take that.
- we've committed that HF will work with 90 days of data
	- note calculations do not support that currently on the fixes in 1.65
        _ it's not clear to me how anything in 1.65.1 helps achieve this.
_ they have hung their go live pre Christmas off that assumption
_ their plan is extremely shaky
- they are going to rely on some manual process TBD to cycle the convosets
	- it sounds like maybe Deloitte are on site to later and going to be doing this for Definity?
- there is a commitment in the future to expand to claims and 10x the volume?  So 100M data points?
_ this seems unsustainable without something like in tool data dehyrdation - i.e basically managing the rolling window for them @mathieu?
       _ the requirement to have all the data there, and also have all the data clustered and investigable etc seem just in conflict to me.
- for this existing use case we're committing some time in January for it not just to work with 90 days, but the full volume without the manual process?
_ we have a new build requirement for the next phase on this uncovered data auto discovery that may or may not be agreed to?Stephen  [12:45 PM]
These were the actions from last night
Next steps
Matt: send Stephen end point changes Maxime making (Done)
Stephen: Example end point testing tomorrow
Urvashi: List of use cases would like us to review for testing on representative environment
Maxime: Making end point parameter pass change tomorrow as well - reach out if need additional time/help
Urvashi: Setup topic business presentation for next week,
Alex/Anand: Talk about new requirement for auto labelling
- tool already supports human in the loop uncertainty clustered labelling flow - this was part of core training with AA and Deloitte team.
- prompts/pipelines/dag can be used to filter for uncertainty, and auto label with an LLM instead into a report - can demo example but would be built in similar way to other reports
- Matt/App on call unaware of any requirement to build anything into core tool



All: 15:00 EST interactive testing session
Run everything end to end
Take timings with fixes and changes in
Experiment with batch sizes
Produce numbers to allow a prediction to be made.
Plan based on those.[12:46 PM]As predicted - immediately failed to do any implementation and stopped work
Thanks for the notes, Stephen. Could someone from the HumanFirst team please share the sample code for endpoint testing? This will help Maxime expedite the code changes. It would be ideal to have it by tomorrow morning so Maxime can use the day to integrate and test it.If they provide the DAG code I'll run it through some AI and manual effort and map out where the calls are and the logic.
Good morning. I've picked up looking at this parameter (await_next_index) today on the representative test environment - there are couple of ways and calls it could be used in the flow.
One of the things I need to do to give you a precise answer is to align all the HF calls (in order and with any loops etc) with their respective DAG and purpose.
Do you have a swim lane diagram or similar with this on already?
If not - can you provide a complete copy of the DAG code I'll go through as quickly as possible mapping this out so we have a documented understanding we can use to suggest where and how to add this.This message was deleted.Stephen  [1:21 PM]
Thread on implementing await_next_index
Matt forwarded on two files from Maxime - only went to him and Sam.
Turns out one of the reasons Deloitte have been so coy about whether they updated to 2.0.0, is that they don't actually use it in some circumstances looks like they've cut and paste the code into their own set of helper functions (edited) 
2 files hf_client.pyPythonhf_utils.pyPythonStephen  [1:26 PM]
@dubois
Latest numbers are 90+ for sonnet and 76 (forcast range 70-75) for NBS - Oliver and Nipuna are finishing up today and tomorrow.  That brings them both up to similar levels to the other reports which the business has accepted.
I will prepare a slide ready for the business.

We have had to bend all sort of things to do this and it will be very overfit to their "baseline" test set.  Realistically it still needs the full rebuild to correct the mistakes built in by Deloitte but that needs a longer and more calm discussion on when, how and how that does or does not get done.

We are expecting to support Deloitte in presenting to the business next week.  There may be questions and answers etc, but...
This will mark the end of any functional work this year on reports, or models.  Leaving just the performance and go live elements to support Deloitte with.
Should the Definity business have any further requests for change, or tweaks, the answer will be No.

Could you make sure Anand understands and is aligned with this to avoid any distracting elements in the call tonight.   Deloitte will need to be tightly focused on the immediate actions they  need to do if they want to have any chance of taking a version live pre-Christmas. (edited) 
appaquet  [2:04 PM]
@Stephen What kind of manual use Definiy has in their workspaces? Do they use the data view & explore data by utterances, or do they always work at the conversation level?
Stephen  [2:11 PM]
Usage patterns not hardened so an opportunity to shape.  Here are the major things they need to be able to do (IMO)

Click through from a report and find and read in a nice format conversations involved in that problem - currently this is based on metadata uploaded to utterance level or annotated using batch actions / columns to the first utterance.  That needs untangling to let convo level only.

Search for conversations where a certain thing happens - again currently utterance level but could be made full index search on larger documents

Then the big one - explore by uncertainty the “other” below clips contents of their charts.  Ie explore which classes they are missing.  This is done based on the output of the pipelines.  So currently it involves a second workspace to be done.  Columns could take that to metadata on original convo but again that is currently utterance level.  Then they rely on the uncertainty and closing flow on the produced output.  But that could also replaced by this new postulated feature Anand/alex discussing 
Stephen  [2:14 PM]
Basically if you think about them looking at the resolved not resolved and class coverage example from document to insight doc.

The questions a user has is

Are my business actions to change this chart working - ie is the resolved number going up.

Are the known categories of problems I am tracking going down?  If not why are they going up?  Jump to real examples of those convos.

Then as known categories of issues go down, the “other” not classified bucket become more significant they want to jump to it then see groups of problems they can start to track and address.

Currently this is where the search and clustering bits really kick in - but they don’t have to work as they currently do.
mathieu  [6:04 PM]
@Stephen for awaitNextIndex, I forgot if I mentioned it, but we didn't add a new flag, it'll be the new default behaviour. if an index is not ready, export will wait for its readiness before downloading data
Stephen  [7:56 PM]
@mathieu question please:  what things trigger index download exactly now post lazy download change?
i.e after I've uploaded a file to a convoset (no-one logged into any worksapce) if I do no other action my understanding is that no indexes would be downloaded to any workspace.
So if I went to a workspace in the GUI and went to PxD/Data Source it would show the spinner as it downloaded.
If I wanted instead to trigger download in a controlled way on each workspace attached what would be the best API to call to make that happen?Stephen  [10:35 PM]
Nicely managed session @dubois thanks for being on
dubois  [10:35 PM]
No problem, lets get out of this fucking thing haha 
[10:36 PM]But we need to stay positive as much as we can its the only way we can get thru it 
Stephen  [10:40 PM]
Well - that's the thing isn't it - and something we need to talk about some more.
If we are on the hook for the quality of results, we have to understand the specification of the requirement we're trying to hit.
That means it's either documented up front and we sign up to it, or if we're defining it as part of the project  we control the client management for defining the requirement and we do that in a way we know is realistic.
You can't have one party accept and create any requirement they want and then have another party be on a never ending hook to deliver all of it.dubois  [10:41 PM]
I completely agree. Speaking to Anand in an hour to make sure I tell him this
Stephen  [3:39 PM]
Testing update:

implemented no_trigger in testing scripts - seems to work - maybe makes list conversationset weird if you haven't done the with trigger at the end - i.e does that report right or wrong - but have not delved into.

Built data multiplier to resuse May/June ABCD into future days whilst maintaining utterance uniqueness.   That enables to roll the date as far forward as necessary

Tested with 60 files loaded and pipelines loading 4 files with no_trigger ~ same dp as 1 files for definity at 400 convos.
~ 70 seconds for trigger when triggered to run on last convo.

Pipelines then executed in sequence
Currently doesn't seem to find any rows when downloading data after pipeline runes - trying to debug.Nipuna  [7:59 PM]
Sonnet Model Update

Finished and changes merged into DEV workspace
58 intents → 95 intents // 2021 phrases → 4385 phrases // 88->89 F1 score
Estimate over the full test set is 88-90% correct (eval sheet attached)
Updated slides with full taxonomy and change log (model diff sheet attached)

Stephen  [5:57 PM]
Parallel testing results
TL:DR

seems to work as expected.  
Is probably slightly slower than running things in sequential in a controlled way.
you can still mess it up by endlessly creating pipelines faster than they can run.
there are a wide variety of edge cases which are very hard to test for


Detail
Wrote parallel testing scripts.  It really depends on what you are trying to run in parallel.
Done various combinations of and not got any failures - the key case is.
File upload + pipeline + download all in parallel - works, but you obviously get no downloads until the file upload finished and then a pipeline finished on top of that indexed set.
Pipelines stack up and run in parallel fine but re all competing for resources.
Whilst running you can try and download and get sensible results (i.e none), but all on the old iindexes as new ones not triggered to build as pipeline not finsihed, then you get results.
If you keep starting pipelnes faster than they can finsih, i.e if you frequency is 15minutes, and your average duration is 16minutes, you start to enter a cascade failure.Stephen  [6:17 PM]
@jay here is the PR for all the data generation, loading, testing sequential and parallel ready for session tomorrow.  https://github.com/zia-ai/academy/pull/141
Code is a little rough - I'll try and do a polish pre-Christmas for README.md docstrings and flowerboxes and what not, but they are functionally sound and reasonably intuitive to use.
Aim tomorrow will be to run through end to end how I've been using them, the multi dim org, generally the sort of outputs they produce etc.
I'm guessing we'll get a key overview and some demos done tomorrow, and can set up further sessions so you're comfortable with making a plan for how this moves forward into E2E testing, or some other phase of testing in the future.#141 WIP Multi Dimension Data and Example Usagezia-ai/academy | Nov 21st, 2024 | Added by GitHubStephen  [7:59 PM]
Deck for Definity session.
https://docs.google.com/presentation/d/1cvd5NCdy_q6fZFu-yNgLjK2tFO5YLFSabgFrF9ilL8Q/edit?usp=sharing
Plan is Nipuna is going to present 1-23 is same level of very comforting detail he has for other three reports.
We will send their spreadsheets and at least this part of the deck after.
We will go to 24 if appropriate being clear how we are continuing to support them through their testing and the fixes already delivered
We will brief them on Nipuna vacation starting this week.
And very nicely let them work out that there is no resource to do any more functional changes, unless they or Deloitte do it
We will do 26 through 42 only if directly asked questions - this will probably be more for Thursday - it covers the granularity and what they may chose to do for BTS calls and the representative testing environment.
There is a Deloitte call directly after.


Stephen  [11:09 PM]
We agreed Rohan on the call is going to do the work and I will review his work. (edited) 
[11:10 PM]Fundamentally it is reading 24 calls and making a decision against the requirements.  That 56% is rubbish.  Urgashi Rohan and Steve had all come to that conclusion on their own. (edited) 
[11:11 PM]We cannot have this ridiculous situation where we go to a meeting have an agreed situation and the assumption is some text suddenly magically undoes what took hours, days or weeks to get there.
[11:13 PM]Rohan will do the work as agreed.
Stephen  [12:08 PM]
@Nipuna I didn't see a CC with the part of the deck presented and the spreadsheets go out - did it get out to the business yesterday?
Nipuna  [10:05 PM]
Walked Rohan through merging FAQ/SrA to PROD.

Told him to double check all prompt/pipeline settings ect but we did a first pass and looked good. 
FAQ model has been moved to prod from QA, SrA has been moved to prod as well with revisions setup. 
There is a batch conversation set linked to each and we uploaded a simple txt file to ensure the conv-set has a convo-src id that API can pickup.


On SrA we spent 5mins on it b/c I said finish the baseline and talk to you @Stephen instead of me.

What its looking like is Rohan / Steven (BI guy) coming to the conclusion that there is clear ambiguity in most of these "fail" cases and you could say either class is correct.
The business didn't provide clear definitions or a prioritization list at any point in the report either. 
Rohan plans on finishing the baseline by checking the calls and sending observations to you, and then eventually presenting to business saying its unreasonable scoring.
(edited)
Nipuna  [10:32 PM]
Rakesh sending an email on the testing for TOPIC raising 3 points (Stephen I forwarded since your email was missing likely due to original chain):

1)Incorrect Column Utilised for Validation:While analysing the NBS results I have noticed the column for QA reference data was wrong.From the sheet shared from the QA team you should be utilizing Column K to Column P for both the excel sheets.I have noticed due to this you have assumed the wrong data used by the QA and it will surely affect the percentages you have calculated for the assumptions made for your analysis.
Example:
Refer the call id 600000009162159 for NBS as a reference for this issue.You will notice you have two predictions made by QA wherein the expectation is only one expectation.

2)Drop of Predictions which is not present: There was a drop of 30-40% of predictions seen which were missed from the QA analysis.As per my investigation I have noticed that the results which were highlighted was never loaded into BQ.For example I have tried the following conversation ids:
a)Conversation ID: 247bbb78-6261-51ca-9603-d3a971428ee2 .So in BQ u can see only three predictions while in your sheet I can see five.
BQ Screenshot:

b) Conversation ID: 247bbb78-6261-51ca-9603-d3a971428ee2 .So in BQ u can see only one predictions while in your sheet I can see eight.
Generally the missing id issue is a Deloitte problem
First point seems to be specific to the Sonnet id 247bbb78-6261-51ca-9603-d3a971428ee2. 
The second id is from the NBS id (copy paste is wrong, below id is the one) fda6083b-fdad-5b9b-8dcf-1c53d55ab70d 


3)Confidence Score Mismatch:I have noticed the confidence score populated in the excel sheet vs the one I have noted is not matching.I believe the column F in the Sonnet_Eval sheet represents the confidence score you see for the QA run.That score doesn’t match the score I identified in BigQuery.It would be great if you confirm this assumption is correct.
So Rakesh is correct here the confidence scores won't match b/c column F in Sonnet_EVAL sheet is from the Nov11th model (latest one in DEV that wasn't trained before we made the changes - hence the diff in confidence score from what he sees in QA BQ)


Stephen  [1:28 PM]
Deck I plan to go through this evening with Definity and Deloitte
https://docs.google.com/presentation/d/1JgDKvlGkcvcpt9ZlvIzo6SYENlFoaHV3ez2hZtSHLK8/edit?usp=sharing

TL:DR parts are.

R 1.65.1 estimated durations


HumanFirst elements of Day to day processing represented in the Pseudo code estimates at 90 day volume for 1 x 400 convo file.
File upload and indexing < 10 minutes
Per pipeline on 16k DP ~ 6 minutes (highly data and LLM dependent)
Index download < 90 seconds

Batch loading predictions.  
If utilising full no_trigger process it should be possible to load 30 days of data in <3 hours including processing all pipelines (LLM permitting)

Index scaling highly linear with datapoints increase
File loading scaling better than linear with datapoints increase
Parallel execution probably slower than sequential




MSA Recap


5 users
1M conversations across all environments and conversation sets.
1 namespace - your environment already upgraded FoC to unlimited namespaces to allow for data segregation and reorganisation
Bugs/Feature Requests/Questions support via the portal https://zia-ai.atlassian.net/servicedesk/customer/portal/1
Availability SLA
4 onboarding sessions
Monthly 1 hour workshops.
No consulting services included. 
Google Slides Multidimensional small file testing analysisGoogle SlideStephen  [3:28 PM]
This is the workspace needed to run tests.
https://studio.humanfirst.ai/playbooks?namespace=multidim

Clickthrough to different dimensions of analysis in Definity Folder for both theirs and multidim.
https://drive.google.com/open?id=1CuasordIcfI-Qz1bFwspyBoqHJHxNH1d&usp=drive_fs

Document to insight walkthroughs
https://drive.google.com/open?id=1t_uybNOm9DIitxUfgHLpDWqvrNj88ftd&usp=drive_fs

Code is committed to academy master.
https://github.com/zia-ai/academy/pull/141
#141 Multi Dimension Data and Example Usagezia-ai/academy | Nov 21st, 2024 | Added by GitHubStephen  [5:25 PM]
Just to elaborate on some strategy for this today so people are aware of the threads trying to hold this together.

representative test environment means if there are software bugs we can test and fix them there - we don't need to use to Definity namespace at all.
we're doing super professional walkthrough of the software/performance fix to show how well we do that.  Through that remind them of the MSA commitments we do have and how we are living up to them through that.
Remind them that MSA says "No consultation services" recap the on-boarding we've done and are finishing up.
We know we have no other work orders or commitments - what's in the MSA is it.
We're going to still support Definity/Deloitte when they need to press know where to press a button, or button doesn't work - but they have to start doing the thinking and the doing.
So the litmus test now is if the work is a) in a spreadsheet or b) about working in their namepsace - they have to be the ones pressing the buttons and doing the thinking.  If it's a bug in the portal or we need to show them something in our workspace, or test something there, we do that in the representative environment.
Doesn't matter if it's Deloitte or Definity - it can't be us.
It's very important we all hold the line on this.  Anand is going to throw all sort of mud and ridiculous statements
If we waiver in this - the situation  will become immediately unrecoverably untenable.
We don't want or need the ICBC business, and even if Definity decided to stop that would be less bad than being on the hook for endless free effort.
(edited)
Stephen  [9:58 PM]
Finally - finally they understand the actual end to end process.
For note - that testing step we always did was the bit Deloitte skipped and buried the results for Topic hence why it got in a hideous mess. (edited) 
[10:00 PM]@mathieu @appaquet @dubois this call is a fantastic example of how  absolutely crucial easy and fast test set establishment, and iteration and evaluation is.  (and requirements establishment) (edited) 
mathieu  [10:13 PM]
https://zia-ai.slack.com/archives/CQBP8UMU2/p1733605993363789?thread_ts=1733605635.535319&cid=CQBP8UMU2

pipeline quirk over the weekend
/indexed failed at 21:03:22Z (worker died), retried at 21:03:31Z (finished at 21:07:29Z) but pipelines fired in between failed immediately because of the previous failure.

they have a running pipelines since 21:09:48Z on that workspace, so it seems resolved for now
From a thread in pipeline | Dec 7th, 2024 | View replyStephen  [10:17 PM]
Righto - E2E testing with Rakesh directly after the Deloitte meeting tomorrow.  He said he’s been having retries so sounds like something been going wrong but hard to say what. 
Stephen  [5:40 PM]
This is what Deloitte have put up on screen in the call.  Encouraging them to think through what is happening at each stage and what it might mean.
image.png Stephen  [6:33 PM]
Actions
Stephen: check with Dev team why likely not hitting quota maxes - maybe guessing because the actual active part of the run is very small?  But LLM quotas don't seem to be part of the problem
Urvashi: check with Maxime why not waiting for file triggers to completely finish before starting next step.

Observations
Selecting the data seems slow.
Caching checks seem fast.
LLM runs seem quite fast through data to be processed.
Indexing seems slow after pipeline finished.
Index downloads are slowish/repeatedly on screen but finishing in 30s



Selecting the data to run on seems to be one of the slowest parts of the operation.

FAQ has probably lots of filtering.  My performance test runs had the pipeline just run on everything.

Are the search predicates making things run a lot slower @appaquet @mathieu?
Stephen  [8:10 PM]
next call.
Starting with trying to get Rakesh to be bale to login to HFStephen  [10:33 PM]
@johnnie just from what I can see in the way they are running things that selecting of conversations seems particularly expensive for Definity - way more than in my test cases.  Maybe they are bigger and uglier, maybe it's because there is so much contention with the parallel running.

How is the batch selecting looking?


Ttrying to work out why Definity so much slower than multidim performance test predicts

Here is my idea list based around looking at the differences with status @mathieu @appaquet incase you have other thoughts.


gpt-4o v vertexai claude - the execution time is a small portion but could there be something about the metadata brought back from vertexai rather than opai that makes the conversations so much more difficult to deal with in a pipeline?
could change perf test to vertexai/claude and rerun

are the conversations just much bigger and uglier than ABCD so that just using 4x as much ABCD isn't actually representative
do data analysis of average tokens per utterance and number of utterances using actual data in there - don't rely on Rohan numbers

is it just the parallelism they are using that locks out thier pipelines on something
trying to get them to run in sequential (in progress)

 they are filtering on multiple pipeline metadata fields inputs does that make it much slower
 added pipeline filter on one ABCD report it just seems to make things quicker as data selected is less. (Done)

Stephen  [4:53 PM]
Mapped out across the different timelines across a full execution window what's happening

according to the pipeline reports across the different workspaces
according to the GUI for the longest running pipeline.


The pipelines are being triggered at almost exactly the same moment when the file still has 3minutes to index.  Then the slowest pipeline only moves quickly, when the competing pipeline stops exectuting.  Other points are suspiciously aligned too.

I think Definity are mostly just measuring contention - trying to get them to separate the execution windows out so we have some clean data


Stephen  [9:15 PM]
OK - very surprisingly productive call with Deloitte.

Maxime has understood the dependencies between file upload and pipeline runs, and is going to start checking the file upload trigger completion, only put the data in BQ when that is done,  and is going to stop the insight DAGs from running if there is no file by checking BQ to find - i.e indexes still running.  They don't want to stagger starts (which I still think is a good idea)  but if they aren't triggering runs that can't work by checking BQ that solves our direct problem.

Stephen: help document how they could - Do their unlinking and linking for 90 day sets.
Also their new (good idea) of doing the rolling window and then having a by the side experimental set by month.

They don't have a plan for catchup load yet, we need to help them build one.

SRE results have been rejected - Rohan work said as designed  86% business has said no, checking again 60%.    This is basically "we don't like the results we actually meant this"  - that's fine but that's new requirements.  This is after previously signing off, requesting changes and signing those on.  There is no way that's getting done this year, we need a plan agreed with them in detail with named committed resources by whatever party providing and working directly with the Definity business to agree what they actually mean now.

I have been very clear we won't be doing any functional work at all until that is in place.  We are moving everything we can to get non-functional things cleared, so they have a go live and real data being looked at which then any functional changes that may be made have a live framework to fit into in the new year.

Net result is FAQ only is going live before Christmas.

Stephen  [11:26 AM]
I was asked to put together a bullet list of the barebones of features/changes needed to successfully run a project like Definity.  This is a short version of the Document to insight docs, and the Nesto ABCD prototype - which are available if and when this is looked again.

If it is looked at again I'd strongly recommend picking a sponsor user - perhaps from the team working at Deloitte or Definity to validate what they would want to see.  As deliver calms Anand is starting to better articulate useful input into what he might want for a future product.


A file can be uploaded and HF manages all the dependencies and produces the end to end insight. (I.e no writing an external pipeline to manage HF internal pipeline).
A User see in the GUI what each pipeline run processes and any slice of the up to date insights - what the APIs produce is comprehensible from within the GUI.
HF manages any rolling window of data for active investigation. (Dehydration or arching)
Conversation format allows multiple role types (sort out client expert, User Agent, allow system messages or multiple users.)
Batch actions work.  with some way of data being auto annotated back to conversations in conversations.
Prompt versioning
A classification model in one workspace to produced insight column of another workspace - and vice versa the output of any column can become the input in a separate clean workspace
There is at least some method for being able to mark a test set and do an evaluation.
Treemap works on any given column
Some sort of way of monitoring the status of all the dimensions of analysis on a single conversation set - ie see what is stuck and fix it
more sensible embedding options (even if basic turn off) to allow avoid embedding input and only embed output.


Looking at this list it seems impossible that this is achievable in Q1 or Q2 with current resourcing and the priorities necessary for Canam.

Particular pinch points are:

Dev understanding of these use cases
The usage patterns here are complex and need FE and BE changes.  The Dev team has little awareness of them and the nuances of their implementation having been very highly focused on Threads for several months.  It is extremely unlikely they'd be able to disengage from this, engage with these, write suitable user stories, plan features and deliver them whilst also doing the same for Canam.

Test resource
We only have one tester in Jay, testing will be vital to a successful public launch of threads and Canam scaling.  It seems impossible a single resource would be able to understand the above, and write suitable test cases through them as well as succeeding in doing Canam.

UX Resource
There is a lot of focus on other ancillary integrations like Zapier/Make and focus for the showcase on success E2E production of things like Kaisen++, Weekly Email Summary.  The user journeys through these are complex and take time to understand what features and part of the value chain HF is going to provide.  It seems impossible that with one UX resource in Callebe he will be able to successfully manage the Canam asks and understand and deliver the same for Analytics use cases.Stephen  [8:55 AM]
Matt sorted out Deloittes go live query (18:12 GMT) from Friday evening (I had no idea they were planning a Friday evening go live) at about 17:07
The pipeline has indeed run on 0 data, you can visually inspect the input filters in the product by clicking "Show input query" (see screenshot). In this case you are filtering for "communication_channel" to be equal to "phone" while your data has its value set to "PHONE".Didn't seem to come back up so I guess sorted.
Stephen  [8:57 AM]
I've written this exercise based on the Resolved dimension of multidim and the Document to Insight set of documents for Eshan's Shreyas and Summits training session on Monday.
Going to ensure that they can create and tune their own Prompts and NLU models from scratch so they understand the full process before they try and do it on any of the Definity stuff.
@John is there anything that I can look back on to what they covered in their first three sessions?
https://docs.google.com/presentation/d/10iM7vRz-Lq5uKtn9Fjpp01m3dwRaR1hofXQmkGQQ81U/edit#slide=id.g2699bd2dc47_0_370
Google Slides Document to Insight Training ExerciseGoogle SlideStephen  [8:54 PM]
Eshan reached out and said Deloitte had double booked over our slot this evening, and pushed our session back to tomorrow at 16:00.
Will login to call just to check no-one turns up.Stephen  [6:36 PM]
Excellent Definity session with Advanced Analytics Team - Shreyas, Eshan, and new lady called Lillian
Shreyas had come prepared, they really liked it being in a safe namespace and on test data.  Shreyas got right through to a CIDER like prompt, the other two going to follow up and get to same point.

https://us02web.zoom.us/rec/share/Qg2Nk-cP7dbxYq9PXrgWqJfejeH2P-dW-loBR_vlZvj6IbLtkpdADojg07p6SkkR.Y4WKx1-mUiCa2I89?startTime=1734451441000
Passcode: Z6^Cwm1zStephen  [9:01 PM]
Tuesday call
image.png Stephen  [9:05 PM]
Call thread - Deloitte asking question about FAQs
image.png Stephen  [9:43 PM]
Summary:

Deloitte have a bug where despite there being predictions in HF sometimes whole files and sometimes individual records don't get back into BQ - Maxime looking at.  Production loading stopped whilst they do to new year.

They are trying to work out again where they have no prediction, and again have forgotten the cases when they get none from Dev and Test. Encouraging them again to write BQ checks for 1) All AGENT turns (can't find in data sources or generated), 2) Too Short (i.e one Agent turn which is sort of a sub category of first) and 3) too long (where they will find in data sources, but the LLM will never be able to predict)

Data has grown to
102 files - some descrepancy between the number of files we show - and the number of files Rohan query has
18 days data, 1.5M datapoints

They were running quite happily but had then some issues on some DAG - seems like was happening simultaneously.
EX_conversations_humanfirst ran for 6 hrs - "triggerId":"trig-5RKVXAPW5BDPXHKTI722IDPR"
IN_humanfirst_insightsfaq failed - trigger ID 'trig-EUSIXHTLPVDWVDOBOLKL25L4'
Screenshot of pipelines in HF

There is also a 3h one.

The fact that both file upload and pipeline are finishing at same moment is suspect to me.  I'm guessing we may well have an issue here - Possibly the Tantivy problem @mathieu ? (edited) 
image.png Stephen  [3:43 PM]
Quick summary of what’s happening 

Deloitte have a plan to get one report running in test on top of FAQ each week for three weeks.

As they do that I’ll need to monitor the interaction and help plan how their stagger those and the interdependencies.  

We know we have seen recently and during that need to be on the watch for

some Tantivy errors
Some jobs running for a very long time 


I will be setting up the follow up sessions for advanced analytics

We should also have Olivier and Riddhi back and primary aim is to make sure they are back doing the actual functional work so will try and setup sessions with them.  

There is then a new plan for the business feeding back on reports in live this is going to generate a lot more functional questions and evaluations changes.  

But it may head off / replace the outstanding Rakesh equations on Topic. 
Stephen  [9:36 AM]
Rohan - Mon, Jan 6, 10:07 PM (10 hours ago)
I am writing to seek your assistance regarding an issue I encountered with one of our conversation predictions. I was reviewing the predictions for a particular conversation (id: cef194ae-2232-5cd0-bb0c-a478d9a0af22), and I noticed that the predictions for this specific call are missing from HF and BQ.Checked it out can't see anything wrong.
Having a look I see 3 FAQs, 9 total outputs (Question, Reasoning, Snippet) generated for Prod FAQ report for that conversation.

Deep link here - you can use these (just copy and paste from the URI bar) to also share the filters you are setting which can help speed up debugging. Here I'm filtering generated, for conversation file: 20241217t211529z_400.json and sourceConversation: cef194ae-2232-5cd0-bb0c-a478d9a0af22 in Inferred_FAQ_Merge_Model-PROD workspace

Happy to have a deeper look, but right now I can't see anything untoward. Let me know if I'm looking at the wrong thing.Stephen  [8:54 PM]
Had a 1:1 with Olivier welcoming him back and bringing him through the two main decks - first one on the performance fixes and multidim workspace
Second on the key aspects of the Loading Plan
Explained Nipuna no longer on project.
Started project to break down a way of getting their cycle time way down and results in the tool based on MultiDim.
Managed to get the first parts sampling conversations from the large prod set to small easily going with minimal SDK changes (one optional parameter)
Off to the Deloitte call now, they would like to discuss the archiving plan - we never got detailed feedback on it pre christmas, have reminded on deck and asked them to recap in prep.mathieu  [9:05 PM]
are they doing their massive backlog runs yet?
Stephen  [9:09 PM]
Call thread
Stephen  [10:59 PM]
Call Summary

Deloitte had an issue where they weren't getting predictions for approaching 20% of the calls, and weren't checking against the known exceptions (i.e too long, too short all agent).  They've traced that to a bug and have readdressed and got the queries to make that change down.

What that means is that they are going to delete all the already loaded data (1.5DP) and reload the existing FAQ report, and then SRE with it.  Aiming to go live with the second report next week.  @mathieu you'll probably get an email from Urvashi, she was asking what the January performance improvements planned were, I said that the IO change in 1.66.1 was the last immediately planned one I knew about in the near term, and that even if there were more having a plan for their data load was still likely necessary.

That plan then is that they've looked at our suggestions and come up with a new one

live convoset with N reports pointing at and a 30day rolling window.
catchup convoset with 1 report pointing at which has a 30day rolling window until the live window is reached
monthly archive convosets with no reports pointing at which are available
BigQuery connector when the client wants to pull in previous BQ data (if they ever do)
This seems fine to me as it limits convosets with many reports to just 30 days, and convosets that are running hard to catch up to 1 report with 30 days, and still maintains the archive with everything in which Deloitte wantd.

They are then trying to do a new BTS report to avoid changing anything from the (sort of signed off) Topic report.
But that's very likely to result in a state where they end up having to redo topic anyway.
It also is going to make maintenance virtually impossible with more complexity layered upon existing.
So they have agreed toinvestigate doing the BTS new report on all the calls - with Intent/Reason split and the prompts fixed at the granularity the client wanted in their new requirements (rather than just doing it for a subset which has to be stitched back in) - I'm going to assist Olivier starting on that tomorrow.
This will be on the 1.5 DP already loaded so we have clean data to start with which wasn't possible first time round.
We can also check it's going in the right direction whilst the existing Topic goes live as is.

Separately I'm pushing on with the faster test set generation and somewhat automated eval so they can iterate faster and we can have a lot more control over what is and how what is tested.
Stephen  [2:41 PM]
Built all their new workspaces for the BTS/Topic Rebuild.  Ran all of the production data their loaded so far to work on.  Drafted prompts for them, outlined process for establishing a testset and managing the client
Details in thread.Stephen  [8:34 PM]
Had a good session with Olivier - he's got his access sorted now, and was into the tool.  Having looked at the production cut of data he's going to go back to the original large dev cut which has samples of conversations across multiple dates and languages.  That's fine as we couldn't find the test convos from Rakesh anyway in the prod set and they are going to rerun.  He's starting with the stripped back split INTENT and REASON prompts and now adding back very specific things that he thinks are needed.  He has a session with the business tomorrow to try and discuss requirements for these new "BTS" Topics - going in more detail to things like "Quoting vendor" "which system the broker has issues with" (currently we say system, not Guidewire or Core logic) and "document types"

Very good to have him back, he's focused on this and concentrating on how to manage this through successfully, rather than testing being all over the shop.

In other news there is a rumour Rakesh (QA lead from Definity) may be moving onto other projects.  This may be a good thing.