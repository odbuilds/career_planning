Stephen  [5:31 PM]
Summary of project

Digital Mortgage Lender in Canada
https://www.nesto.ca/
Sold through SECloud experts
https://se-cloud-experts.com/en/

Is a project to analyse a large amount of call data.
+ we only have to do representative section.
- document reads as the start as if we need to do transcription, at the end seems to be big query.

Key deliverables are to extract:
* the overall structure/steps followed by the sales rep in the conversation,
* whether the sales rep is respecting the prescribed playbook or sales methodology, and
* overall consistency across sales reps
+ can probably do, but have not seend the Prescribed playbook(s) or methodology to know whether this is going to be practicible.
- is a first of class project

Also includes producing an additional dimension of client analysis.
- means we'll have to find something unless their save it - presume key issue or something like that.

Project will be in English or French - TBD

Has DialogFlow CX on the Architecture diagram but won't be used in the project - does mention Vertex elsewhere.

Acceptance of deliverables 5 days after receipt automatically - must redo any comments.
- is dated 1st of Aoril with +/- 5 days with penalty charges for changes.
+ Billed up front, but with acceptance at end?

Has the following roles for delivery:
- unclear who is down to provide which.

Account Manager
Project Manager
Solutions Architect
Cloud Engineer
HumanFirst Expert


Stephen  [4:01 PM]
@dubois transcription per hour - assuming we can send their data to the cloud.
$0.30 crappy $1.50 best per hour - we'd use best all the time because it's just so much better
If we can't send to cloud it's still about the same in GPU costs but there is a lot more setup and time involve.25 repliesdubois  [4:27 PM]
this is just to cover costs right? We’re not making margin on this
Stephen  [4:27 PM]
This is just GPU/API cost.
[4:27 PM]No time add, no engineering, no pipelining
dubois  [4:27 PM]
ok
[4:31 PM]Could we enable Nesto to do it on their side?
[4:32 PM]or too difficult (they’re technical and pretty smart)
Stephen  [4:32 PM]
https://www.speechmatics.com/
SpeechmaticsAI Speech Technology | Speech-To-Text API | SpeechmaticsSpeechmatics offer the most accurate AI speech technology - with AI transcription & real-time translation components. Try our Speech API today!https://www.speechmatics.com/[4:32 PM]Create a free account.
[4:32 PM]Send them audio.
[4:32 PM]Use the best model
[4:32 PM]Save the results in a bucket
[4:32 PM]Give it to us.
[4:33 PM]like maybe there is some stuff on diarization we want to think hardera bout.
[4:33 PM]Batch transcription (Pre-recorded)
$0.30/hr
for :zap: Lite Mode Standard accuracy
$0.80/hr
for Standard accuracy
$1.04/hr
for Enhanced accuracy
SpeechmaticsPricing for our Speech Recognition API Services | SpeechmaticsSimple plans, simple prices. Pick your preferred Speechmatics pricing plan. Trial, test & build with the most accurate speech-to-text API via our portal now!https://www.speechmatics.com/pricing#faq-lite-mode[4:33 PM]We should try a small sample of their data first before they spend a lot of dollars.
[4:34 PM]I.e do say 10 convos end to end and check everyone is happy with the process.
dubois  [4:34 PM]
kk
dubois  [4:09 PM]
We’d use speechmatics? What is breakdown if we’re doing it?
Stephen  [4:12 PM]
At the moment if we need to do it in CS I would much prefer to use an off the shelf API - the quality is now as good as anything I've been able to run locally with a lot of hassle.
dubois  [4:12 PM]
So how do we get to 1.5USD per hour?
[4:12 PM]if whisper is .36$ per hour
Stephen  [4:14 PM]
Didn't like whisper API
[4:14 PM]1.5 is speechmatics 1.05 plus a margin for doing it rather than them doing.
[4:14 PM]Also 1.5 per hour is a good market rate - or they can do it and try and work out the best cheapers.t
[4:15 PM]At 1.5 / hour we can afford to try a couple of things and work it out.

Stephen  [10:02 PM]
OK - so trying to get some lessons learnt from a very frustrating day.

Our code
Speechmattics  SDK includes lots of things and doens't play nicely with Academy
Have split it out to a separate venv setup and separated the code into a dir and tied up into helpers

Speechmatics
It looks really good, with like default languages, and expected languages - things which we want.
But the python example batch client doesn't support those options
The batch system also polls where as it says not to poll in production.
So probably need to write our own logic for how we want to mass submit jobs for batch supscription.
Then read the results.

Google Cloud Storage
Nesto didn't give write access.
The easiest thing is to use gcloud storage rsync to keep a direction up to date
Automatic Default Authentication has a lot of assumed stuff.
Then just use everythings there.

Need to get install started
Ata - seems to think we are doing the install?  need to check what the plan was and get on with.
Yes I can help you with enabling new services in GCP.[1:20 PM]Nesto reviewing call logs, but proactively sent this list

Speechmatics scripts have run into an issue where their batchClient SDK doesn't support all the features of the REST API.
So particularly can't send auto detetction requests and fallback language.  Which would be useful for FR, EN
Also it does polling for one job at a time, which is is really slow and not batch.  It also warns not to do that.
Longer term need to rewrite using the base API and create a better batch mode.

Speechmatic scripts need updating to add these as suggested content enrichment.
EN:
Agreement of Purchase and Sale, Amortization Period ,Amortization ,Appraisal, Appraisal Value, Blended Payments, Bridge Financing, CMHC, CMHC Insurance Premium, Closed Mortgage, Closing Costs, Closing Date, Nesto
FR:
Demande de prêt immobilier. Franchise, Montant de votre prêt


OK confirmed they really do want a private cloud managed install chased for Marc to get access with enough GCP privs to do ti.

Stephen  [3:44 PM]
@Marc Alloul Ata confirmed want us to install private cloud and answering with method questions on email now - you ok to pick up and answer?
3 repliesMarc Alloul  [3:45 PM]
yes! I will respond now
[3:45 PM]@mathieu In this scenario, how do you propose we manage the TF backends? Do we put the backend end in their infra and package the TF files used? Do we just install and keep the backend on our end and not share the TF files?
mathieu  [4:06 PM]
I guess the real question is do we set it up in a VM with the onprem package, or do a full GKE deployment (which might be overkill for a their size)

Asked ata for access for @fayaz to GPC.

Need to
get faraz to verify GCP scripts.
Look to see whether batchclient lets content annotation happen.
EN:
Agreement of Purchase and SaleAmortization PeriodAmortizationAppraisalAppraisal ValueBlended PaymentsBridge FinancingCMHCCMHC Insurance PremiumClosed MortgageClosing CostsClosing DateNesto
FR:
Demande de prêt immobilierFranchiseMontant de votre prêt

Marc Alloul  [7:51 PM]
replied to a thread:so far its looking good. I am able to impersonate the service account, haven't been able to test creation of the VM yet due to them not having a default network in the project. I am working on creating terraform files now so that we have somewhere to put the VM.

I just want to validate my understanding of what is expected:


Create vpc for our VM using the credentials provided by Ata
Create a VM 
Provision onprem on this VM.
Upgrade app version on VM monthly


If this is correct, I have some questions:


Was there any previous conversations regarding access to the VM? Meaning do they want the App firewalled to their networks and not available publicly or will our auth suffice?
Was there any agreed upon instance sizing / GPU's / cost ?

Stephen  [9:32 AM]
Great stuff, thanks Marc and talked through this in QA committee and Jay is going to a release level verification when finished.

1-4 - yes

5 - no  additional requirements documented or that I'm aware of.  Can you please assume our auth sufficient and make publicly available.  If they want specific infrastructure design then we should be pricing that in or they should be doing it themselves.  In general we want this "private cloud deploy" to be as close to the cloud experience as possible, so making sure we can access to help them and we get monitoring and stats out etc.

6 - none documented or that that I'm aware of - can you please make assumptions that prioritise user experience based on Verizon experience?   I.e the expectation should be that it's a reasonably expensive beefy box.  So our standing recommendation of 8 CPU, 32GB memory, and 500GB, No GPU disk seems to me to generally be too small.  Verizon ended up adding more memory and disk quite quickly and we are now recommending GPU.  So maybe 8 CPU, 64GB,  1TB, + decent GPU?


heir environment is almost done. Since it is a public facing URL i figured we needed to add SSL to encrypt the connection.
I used a self signed certifcate for the time being, it might be worth asking the client if they have a domain name / SSL certificate they would like installed.

For now it can be accessed here, there will be warning saying the cert is untrusted / self signed. This is expected.
https://34.47.12.14.nip.io
The PW was generated and on the admin PW is present on the server, no sure how we can share this with the client.
As stated above, GPU is not active yet, however all drivers and everything is installed so it should (:crossed_fingers: ) be easy to enable it as soon as the next release is done.

The current version is v1.53.1 (edited) 
10 repliesStephen  [11:29 AM]
Yes, must be SSL!  Thank you.

Can we create n.humanfirst.ai and create a certificate so it's just all managed by us and we don't have to chase for things clients find difficult to provide, and no-one worries about insecurity warnings.  Also avoids having to use nip.io which has been a pain in the past.

Lets try and make the initial impression as good as possible with an reassuring URL and the GPU on 1.55
Stephen  [1:03 PM]
On the password front - as this is managed private cloud, I don't think we would share the admin PW on the box?

Can we create a 1Password store of the admin and keycloak keys etc and share it with the CS team please?
Marc Alloul  [6:50 PM]
Sure, I'll have to check with @mathieu about using our domain for this but I think its a good path to take. nesto.humanfirst.ai maybe instead, incase we have other clients whos name begins with n in the future.

 Can we create a 1Password store of the admin and keycloak keys etc and share it with the CS team please?Sure, ill get this done shortly
Stephen  [6:53 PM]
So I started there but in general we shouldn’t use nesto.humanfirst.ai as we are publically identifying/broadcasting them as a customer which unless they have an agreed case study would potentially breaks confidentiality agreements.  So I shortened to n.  Whcih agreed might have another n in future 
Marc Alloul  [9:32 PM]
ah ok, i understand, I've shared the PW for the current deployment. The URL in 1password is the IP currently. I will modify the entry once I have everything working on the proper domain
https://share.1password.com/s#i4AjYipuBIl4DjfutUJsDC_uijtJ98Q4IFZTcaNB98Y
https://share.1password.com/s#e7C18gr7rgnKCc3IR5mcIBgVg585e3_xd70wbXTNrxo
Marc Alloul  [9:47 PM]
@Stephen After speaking with @mathieu, we think the more secure avenue would be for the client to provide us with a domain and cert if possible.  There is a possibility that the certificate transparency logs can leak information about our other domains and we would like to avoid this scenario if possible.
Stephen  [11:59 AM]
Where it's actually on-prem and they are managing I'd agree, but this is a managed private cloud - basically like studio-qa. not being in control when the certificate needs renewing, or there is some routing issue is going to be an ongoing pain, which having control of the certificates mitigated.

If it's on public internet it has to be secured as much as the public cloud version anyway.

Certificate transparency logs are already public (see attached public list of all our domains and certs).

This is going to slow things down and take things out of our control - can we not just get on and create this?
2024-06-28 List of Certificates.txt 

Google Trust Services   fe28d78c999609fa0d8e70d56cbacb47    humanfirst.ai   2024-06-12  2024-09-10  non-EV  ecdsa-with-Sha256   EC-256  2
Let's Encrypt (43)
    Let's Encrypt   306f60ee4165ba4c847d27091c99ff4cf0c studio-staging.humanfirst.ai    2024-04-03  2024-07-02  non-EV  SHA-256 RSA-2048    1
    Let's Encrypt   4ece61c96f6774878d9dbd886dd577e4995 api-staging-internal.humanfirst.ai  2024-04-03  2024-07-02  non-EV  SHA-256 RSA-2048    1
    Let's Encrypt   3ea75919eb43ddf1640c6e59359a1a2e3fb api-staging.humanfirst.ai   2024-04-03  2024-07-02  non-EV  SHA-256 RSA-2048    1



Stephen  [11:14 AM]
@Marc Alloul now 1.55.1 out can we update the Nesto environment, and give them the secured dns link to login?
Marc Alloul  [3:22 PM]
I will look into upgrading the deployment and enabling gpu support today
Stephen  [4:28 PM]
OK talked through in CS committee - linking up that and since.
Their tech person Ata was away.  Should be back now.
We now have slack connect setup (adding you Marc)
I've chased Fayaz logon and asked the question on domain/certificate as agreed.  If they flounder though I think we should step in and provide


Yes, must be SSL!  Thank you.

Can we create n.humanfirst.ai and create a certificate so it's just all managed by us and we don't have to chase for things clients find difficult to provide, and no-one worries about insecurity warnings.  Also avoids having to use nip.io which has been a pain in the past.

Lets try and make the initial impression as good as possible with an reassuring URL and the GPU on 1.55
Stephen  [1:03 PM]
replied to a thread:On the password front - as this is managed private cloud, I don't think we would share the admin PW on the box?

Can we create a 1Password store of the admin and keycloak keys etc and share it with the CS team please?
Nipuna  [2:43 PM]
joined #末-client-nesto.Stephen  [2:44 PM]
Done the monthly load/balance check - Nipuna going to start on the interactive sessions on this one.  I'm going to continue to try and PM through and get the main setup done.

OK asking the DNS/certificate question has opened up all sorts of on prem network design issues. 
Marc Alloul  [6:28 PM]
https://zia-ai.slack.com/archives/C07APPK7DHU/p1720023474749599?thread_ts=1720016796.218699&cid=C07APPK7DHU
fyi, i will work on this after the update.  I haven't setup IAP before so may take a bit of time.Could you please disable the external ip address and configure IAP please?
From a private conversation | Jul 3rd, 2024Stephen  [6:30 PM]
Ok thanks Marc as long as you are happy to step in here - and you think it’s workable to maintain and deploy images in the future 
Marc Alloul  [6:33 PM]
I think its a fair ask by him in relation to server access via SSH. Especially since the SSH security vulnerability announced over the weekend.
I find it a bit odd that they want to use SSH tunnels to access the web interface though. I will do a bit of digging on my end to determine if we can access the web interface via IAP or some other way if we opt to remove the public IP's all togetherStephen  [2:37 PM]
Thanks Marc, how is it looking?

OK asking the DNS/certificate question has opened up all sorts of on prem network design issues. 
Marc Alloul  [6:28 PM]
https://zia-ai.slack.com/archives/C07APPK7DHU/p1720023474749599?thread_ts=1720016796.218699&cid=C07APPK7DHU
fyi, i will work on this after the update.  I haven't setup IAP before so may take a bit of time.Could you please disable the external ip address and configure IAP please?
From a private conversation | Jul 3rd, 2024Stephen  [6:30 PM]
Ok thanks Marc as long as you are happy to step in here - and you think it’s workable to maintain and deploy images in the future 
Marc Alloul  [6:33 PM]
I think its a fair ask by him in relation to server access via SSH. Especially since the SSH security vulnerability announced over the weekend.
I find it a bit odd that they want to use SSH tunnels to access the web interface though. I will do a bit of digging on my end to determine if we can access the web interface via IAP or some other way if we opt to remove the public IP's all togetherStephen  [2:37 PM]
Thanks Marc, how is it looking?

Update on how to access the VM

The client wanted us to use IAP tunnels, an Ata mentioned that is how they will connect.
Users will need to update their hosts file so that nesto.humanfirst.priv resolve to 127.0.0.1
127.0.0.1       localhost nesto.humanfirst.privLinux / MacOS users will need to run this command with sudo in their terminal and leave it running before opening the browser:
Windows users will most likely have similar command with sudo using the admin terminal. This is required to use port 443. I am trying to get this unsuccessfully to work with a non-priveleged port in order to forgo the use or sudo/admin terminals.
sudo gcloud compute start-iap-tunnel nesto-humanfirst-onprem 443 --impersonate-service-account=gsa-cicd-humanfirst@humanfirst-prod-bb47f202.iam.gserviceaccount.com --project=humanfirst-prod-bb47f202 --zone=northamerica-northeast1-c  --local-host-port=localhost:443

There will be warning due to the SSL certificate being self-signed. We can add the self signed CA to chrome or Firefox if necessary.
https://nesto.humanfirst.priv

This all feels a bit hacky but it appears to be the only way forward with nesto and the onprem VM.
Anyone have any thoughts on this ?


Marc Alloul  [9:11 PM]
:wave_doge:
Update on how to access the VM

The client wanted us to use IAP tunnels, an Ata mentioned that is how they will connect.
Users will need to update their hosts file so that nesto.humanfirst.priv resolve to 127.0.0.1
127.0.0.1       localhost nesto.humanfirst.privLinux / MacOS users will need to run this command with sudo in their terminal and leave it running before opening the browser:
Windows users will most likely have similar command with sudo using the admin terminal. This is required to use port 443. I am trying to get this unsuccessfully to work with a non-priveleged port in order to forgo the use or sudo/admin terminals.
sudo gcloud compute start-iap-tunnel nesto-humanfirst-onprem 443 --impersonate-service-account=gsa-cicd-humanfirst@humanfirst-prod-bb47f202.iam.gserviceaccount.com --project=humanfirst-prod-bb47f202 --zone=northamerica-northeast1-c  --local-host-port=localhost:443

There will be warning due to the SSL certificate being self-signed. We can add the self signed CA to chrome or Firefox if necessary.
https://nesto.humanfirst.priv

This all feels a bit hacky but it appears to be the only way forward with nesto and the onprem VM.
Anyone have any thoughts on this ?nesto-self-signed-ca.crt 

-----BEGIN CERTIFICATE-----
MIIDezCCAmOgAwIBAgIUL25+dDOi248ltMnN9nHa+Y2F8mQwDQYJKoZIhvcNAQEL
BQAwTTELMAkGA1UEBhMCQ0ExDzANBgNVBAgMBlF1ZWJlYzETMBEGA1UECgwKSHVt
YW5maXJzdDEYMBYGA1UEAwwPaHVtYW5maXJzdC5wcml2MB4XDTI0MDcwODE2NDkz
NFoXDTI2MDcwODE2NDkzNFowTTELMAkGA1UEBhMCQ0ExDzANBgNVBAgMBlF1ZWJl


5 repliesStephen  [1:41 PM]
OK catching myself up so IAP appears to mean ~~ SSH tunnelling

So we end up sharing the key manually and adding to firefox/chrome to verify the host.

Have to frig hosts to resolve the name for the certificate to local machine to connect to the tunnel.
Marc Alloul  [4:01 PM]
@Stephen I posted this before the client said they would have a domain name + Certicate. The above is invalid and was done in preparation for them not having anything. IAP is identity aware proxy, essentially they are tunnels made with gcloud commands.
Stephen  [4:01 PM]
Yep - was just catching myself up on my saved later in slack to work out what the old solution was and what the replacement was (edited) 
[4:02 PM]Great that they are coming back with domains etc.
[4:02 PM]This did look hacky like you said!

So this seems to be managing through, I have a workshop with @fayaz on Thursday to do a handover.
Broadly the next steps are for @fayaz

work out if how/if we can access the S3 bucket with the call recordings on using service account impersonation.
does the AWS SDK support it?
do we have to sync the entire bucket locally via CLI (which does)?
Other?

add the Content Enrichment to speechmatics script - these are words/phrases that appear in the scripts that we want the transcription to particularly aware of - note Nesto - without this sometimes speechmatrcs in the "nesto" org examples transcribes it as Nest or NASA.
EN:
Agreement of Purchase and Sale, Amortization Period, Amortization, Appraisal, Appraisal Value, Blended Payments, Bridge Financing, CMHC,CMHC Insurance Premium, Closed Mortgage, Closing Costs, Closing Date, Nesto

FR:
Demande de prêt immobilier, Franchise, Montant de votre prêt


transcribe a small random set and present to client
work with client to agree good enough, any changes.  Then run full set.
work with growth to check who pays (I think we do)
load to environment

Then work with client on Key issue, Resolution analysis.

dubois  [3:06 PM]
Karim wants to figure this out in the calls - could we have a nice prompt ready for testing next week around this scope? :

Among the calls not transferred to a broker. I am looking to find out if the SDRs offered the client a referral to a partner
3 repliesStephen  [3:11 PM]
Sounds like a dooable prompt.

Fayaz been making good progress on updating the access to the scripts.

To get there we'll have need to have done a decent chunk of transcription

@dubois Who's paying for the transcription - is it us?
Similarly with models/keys - are Nesto going to be deciding which model/cost, and providing keys or us?dubois  [3:16 PM]
Nesto will pay for it, but lets start a small batch first
Stephen  [3:17 PM]
Righto so that dependency tgh thing most likely to delay things.

Fayaz can get that small batch run and then an example prompt, but need to have whatever agreement there are and the small batch reivewed to then do enough transcribed to do meaningful work.

So if you could keep an eye on that next week it'll keep progress moving.


fayaz  [9:06 PM]
@Marc Alloul
I am trying to upload a ~10k utterance dataset to Nesto HF. but it seems to be stuck on upload in progress page.

Attaching the file here.

Don't know what's causing this.
3 files image.pngPNGnesto_200.csvCSVimage.pngPNG2 repliesMarc Alloul  [9:43 PM]
Can you check the browsers developer tools to see if there is any error in the console tab ?
fayaz  [5:19 AM]
Hey Marc, today i am able to upload without any issues. Ata increased the size limit which unblocked this issue.



fayaz  [9:00 AM]
@dubois Did they give any list of audio languages that we can expect? I initially thought the GCP bucket had English and French audios only but Speechmatics is detecting Portuguese. Speechmatics could be wrong. Here is the audio file. Listen and let me know if its French or some other language.

@callebe Could you confirm if the audio is Portuguese or some other language?
Waveform Audio five9---recordings---01B2BC8A9B564BF287374ED59BBFB4B9---2024-03-12T122913.wav1:26(1 MB)1:26Allô, Allô allô, Bonjour, bonjour ici, n'attendez chez mon meilleur taux. Est ce que je parle bien avec José? Oui, c'est moi et désolé, je n'ai… 2 repliesStephen  [9:42 AM]
You can use the "expected_languages" parameter with speechmatics passing only FR EN to avoid it creating false positives for other languages. https://docs.speechmatics.com/features-other/lang-id
docs.speechmatics.comLanguage Identification | SpeechmaticsLearn about Speechmatics Language IDfayaz  [9:44 AM]
Did that already. Above is just a manual check whether the "auto" language detection was working properly.


Hello @Karim @dubois @fayaz @Nipuna my first day back and catching up.  I can see the thread on delivery timelines, and it looks like we've been able to make some excellent progress whilst I've been away to make a start on delivery asap.   Just recapping then where we are at so we can be ready to make a fast start - a couple of questions inline if we can head off before Monday to maintain velocity!

Meeting is next Monday 12th, 13:30 EST, 18:30 GMT.

Speech transcription
initial 200 done, now 2000 and in workspace ready for review.
Pipeline updated to include requested content enrichment for key terms, and supports expected FR/EN only auto language detection.
Setup pipeline with extended batch mode - expect full 31k run to take ~20 hours


Environment
appears to be fully setup, HF team have access via a 2-step google SSO + keycloak user
Are you both @Ata Teimoori @Karim able to use the environment OK - are there any other users to be setup?


Example Prompt
Here in the environment - https://humanfirst.nesto.ca/playbooks/playbook-Q67RNGNH7JB7LCMIN7YIIXZO/explore/uttera[…]3Afalse&dataSortBy=date&dataSortDir=asc&showDuplicates=true


LLM
currently using a HF OpenAI key loan key for test prompt - @Ata Teimoori / @Karim in the SoW it references vertex AI - is there a Vertex key you want to use with Gemini, or would you like to use OpenAi for the project?


Intros
Fayaz is going to continue to manage the backend speech transcription pipeline, but as he is on IST (+4.5) Nipuna on EST (-5) is going to step up during the project for any onboarding or intro sessions.   He'll be on Monday to intro in person then.
[3:54 PM]Internal additional notes:

going to add some more metadata to final load - Fayaz doing tomorrow
need to agree costs on transcription in meeting 
Draft prompt looks fine, but the definition of "reference" call probably needs confirming.  Is it just a callback using their number as a reference?   Have cases were people are chasing a callback and then are given some spiel and go on waiting to be called.  
Does it go to broker - calls appear to stop at the point the agent says they are going to be transfered - the rest of the call isn't there - need to determine if enough.
Going to need to create some test sets to validate prompt
Need to know what other things they want to know about these calls.


Stephen  [3:55 PM]
We need to be treating Nesto env from here on in as a client production environment.
Currently it's reporting as 1.55 where as production is 1.57
Can you upgrade it to 1.57 please @Marc Alloul and then how do we make sure that every prodcution release immediatley goes to it as well as main cloud prod?
7 repliesMarc Alloul  [4:24 PM]
sure, ill do this today
Stephen  [5:03 PM]
TQ.  Kick off Meeting is at 13:30 EST 18:30 UK tonight.  Suggest we wait till after to do the upgrade? @Nipuna could you flag in meeting and ping Marc when clear?
Nipuna  [5:05 PM]
Sure yeah ideally Marc we do the upgrade after the call today. I'll keep you posted.
Marc Alloul  [4:33 PM]
is it safe for this upgrade now?
Stephen  [4:34 PM]
Nesto ended up going fast last night and scheduled another call today at 14:00 EST
[4:35 PM]@Marc Alloul thank you for following up!  So if it's definitely going to be finished by then yes, if there is any uncertainty suggest we leave to morrow and start first thing.

That might give a chance to point them that going to be refreshed in tonights call @Nipuna
Marc Alloul  [4:35 PM]
ok! let me know when its safe to do so :slightly_smiling_face:

Scope recap from SoW

SE Cloud Expert, maintains a voice channel where their prospects can interact with their sales reps
and mortgage advisors. Nesto has a large volume of recorded conversation data which they would
like to analyze the following, but not limited to:
● the overall structure/steps followed by the sales rep in the conversation,
● whether the sales rep is respecting the prescribed playbook or sales methodology, and
● overall consistency across sales reps

Benefits
By extracting the above insights from the conversations, the customer will be able to identify areas to
optimize sales call conversion.
This project will help the customer solidify a business case around:
● CCAI
● Dialogflow CX (agent assist)
● Vertex AI/Looker powered analytics and dashboards

Scope of Services
Zia.ai Inc. will provide:
● A GCP hosted HumanFirst Studio organization for use for 6 months
● Ingest a representative portion of transcripts into HumanFirst Studio
● Extract:
○ the overall structure/steps followed by the sales rep in the conversation,
○ whether the sales rep is respecting the prescribed playbook or sales methodology, and
○ overall consistency across sales reps
● Produce a summary for each of the transcripts of the information required
● In the final phase propose, agree and produce an additional summary dimension that the Customer wishes to investigate and produce the summary for
● Produce a logical hierarchical classification for each type of summary
● Deliver to the Customer a csv containing all the original transcripts with the three enriched summaries
● Deliver all the training data or prompt directives that were used to produce the summaries
● Provide access to the prompts and training data into HumanFirst Studio for the Customer to
interact with and examine



● Deliver a presentation including visualizations of the data in Looker and key observations for each
phase.
● The final phase presentation will include a summary of the findings across all phases helping
solidify a business case around CCAI and/or Dialogflow CX and/or Vertex AI/Looker analysis.
● Conduct a meeting to review at each phase the presentation of findings
● At the Customer’s request conduct up to 3 one to two hour training sessions on how the
summaries were produced
After the engagement is completed, Zia.ai Inc will document their delivery and provide recommendations
around CCAI and/or Dialogflow CX and/or Vertex AI/Looker analysis.
Success Criteria

● Zia.ai Inc. have completed all items listed in the Scope of Work and Deliverables sections, with delivery of
an architecture diagram that includes the items in the Scoped Workload(s) sections
● Client agrees that architecture covers components in the Scope of services section.
● Client accepts the deliverables listed in activities and deliverables

Deliverables
Analyze SDR sales calls
Entry criteria:
● Data has been provided to required standard
Expected Duration:
● 6 weeks

Deliverables:
1. Access to HumanFirst Studio to appropriate Customer staff
2. Representative portion of transcripts are uploaded into the HumanFirst Studio annotated with appropriate
metadata
3. The overall structure/steps followed by the sales rep in the conversation, whether the sales rep is
respecting the prescribed playbook or sales methodology, and overall consistency across sales reps
summaries produced
4. Classification models produced in Humanfirst, with F1, precision and recall scores for each class/dimension
5. CSV containing the transcripts enriched with the key issue summary
6. Training data for the classification model and all prompt directives in HumanFirst Studio
7. Presentation including visualizations of the data and key observations of the data in customer’s Looker
8. Meeting conducted with appropriate Customer staff to present and discuss data and observations
9. If requested by Customer: one to two hour training session on how the summaries were produced.


dubois  [8:03 PM]

SDR Analysis (only outbound + preview)
14 SDRs
Asks:
Max to send playbook for SDRs in outbound
Ata giving us exit criteria metric
Successfully transferred to a broker (Y/N)
Karim might add additional things


Recurring meetings
14.00 Tuesdays meeting - Stephen


Stephen  [8:03 PM]
Ata Teimoori
6:53 PM
Preview:
A preview dialer is an automated dialing system that sends a contact record to agents to review before placing an outbound call. This allows agents to review information about the prospect/customer before making the call so they can be more prepared for the interaction.Stephen  [8:39 PM]
Internal Minutes

2024-08-12 Nesto

Ata Teimoori - Director of Data Engineering
Ben Stubbs - VP of Sales at nesto
Max Wegner - CRO
Samuel Couture-Brochu - CPO Chief Product Office
Karim Benabdallah - CoFounder and CTO
In Room
Brian K. Philippe - partnerships (Long Hair)
Gregory Saget-Rudd - VP of growth (Beard)

Max - "priority one - identify coaching opportunities to increasing the converstion SDR to broker"

Date Range is BigQuery SQL 2023 Dec -> + Full 2024

Max: Sending categorisation of SDR list, i.e if people left quickly, to mark and exclude

Narrow scope to Preview and Outbound
Inbound   --> 7260 calls
Manual    --> 617 calls
Preview   --> 10909 calls
Outbound  --> 12370 calls

Preview is:
"A preview dialer is an automated dialing system that sends a contact record to agents to review before placing an outbound call. This allows agents to review information about the prospect/customer before making the call so they can be more prepared for the interaction."

Two reports to go at
- did it convert from the SDR to the Broker
- did they follow guidance

Max: sending Word document guidance given to SDRs

Regular sessions - Tuesday 14:00 EST, 19:00 UK

Sam - asking about Sampling to balance across users
Sam - asking about clustering parameters.

Ata: I can add the flag (successful transfer) to the dataset by tomorrow 2PM

Sam - "Can I compare runs on different models."

Alex Demo of Nipuna Text Bison Tuning

Transferred
Reference Call Offered
Reasoning
Snippet


Stephen: get D call moved (DONE)
Nipuna  [8:41 PM]
For the call tommorow, just confirming the invite should be to:

max.wegner@nesto.ca
ben@nesto.ca
ata@nesto.ca
Should any else be invited or marked as optional?
dubois  [9:52 PM]
invite Karim
Stephen  [11:28 PM]
OK PR to add the BQ data (downloaded to CSV and attached here) to the existing 2000 (which Marc A helped me download)
https://github.com/zia-ai/academy/pull/123
There is 1 blank line after the join - I can't workout why but otherwise perfect.

Relinked to workspace
https://humanfirst.nesto.ca/playbooks/playbook-XYI4EHKIQZFNNPIU4WGS4ZHX/explore/uttera[…]a-cdebfe58-aa9a-44e2-a0f4-bf0cc898e5c3&groupBy=conversation

Ata says he has requested Gemini BLOCK_NONE options - but we can't rely on it being there.

@dubois did you get the Word doc with guidance from Max - can you share it here?
@Nipuna this should let you separate out Preview calls from Outbound calls (and the others) and filter for different agents.  Can you make a start planning the session and seeing if we can make any significant progress on the two reports for 2K?

Important - on another note - I've messed up.
We got excellent traction with Nesto and Max and I didn't want to say no to anything, but wasn't expecting a "lets do it tomorrow".
So the regular slot is going to work and we've shifted Deloitte, but tomorrow is Katherine's birthday, and we have an evening meal out with her extended family.
I'm not going to be able to make the meeting tomorrow or Deloitte afterward.
If I can free time to prep what needs to happen @Nipuna @dubois are you able to run the first session tomorrow, and I'll send my apologies? (edited) 
Nipuna  [11:49 PM]
Yes I think that should be fine. I will get started on some prompts tommorow given we have the pdfs and documents from them. Only blocker is textbison is much poorer in terms of reasoning. Maybe I’ll check with Ata if we can use Anthropic via Vertex.

On a seperate note I got an auto decline from Max’s side saying OOO so I will check tommorow if that slot is even possible for him. 
dubois  [12:09 AM]
@Stephen don’t sweat it man :slightly_smiling_face: Take the time with Katherine, Nipuna and I will cover and worst case we tell Max we move to next week while we wait for Ata to send us the conversion data from calls.
Stephen  [12:19 AM]
Anthropic on Vertex is a really good plan, and thank you both.
Nipuna  [3:20 PM]
@dubois when you get the chance can you drop the SDR call script PDF that Max sent in that email thread. I don't have access to their GDocs via the link
Stephen  [4:49 PM]
Just a heads up Dubois across Deloitte and Nesto - I know you can't see the Deloitte teams chat

We're entering a crunch time with Deloitte with them very nervous about their deadlines at the same time as Nesto wanting to move fast.  Both are assuming basically we are FT on each of their projects.

So they are both competing hard for Nipuna's EST windows for fast responses, and sharing a Tuesday 19:00 (Deloitte) 20:00 (Nesto) window.  So we have deadlines for both today.

I'm trying to add bandwidth in a follow the sun manner in the mornings, and Fayaz standing by for transcription etc.  But it's unlikely we can immediately react to both clients when Ata does pings like today at the same time trying to keep up with Deloitte doing the same.

So just to explain why the re-enrichment is going to have to wait. (edited) 
dubois  [4:53 PM]
All good, I’m fine rescheduling Max to later this week if y’all prefer
Stephen  [4:57 PM]
What do you think @dubois do we need the additional Ata annotation for tonight as we can filter by preview/agents (which seemed the first priority for Max)

Similar @Nipuna with the load from Deloitte today is a push back better?
dubois  [4:58 PM]
Yeah there’s no sweat in asking Max to meet thursday
Nipuna  [5:29 PM]
Yes agreed I want to spend some time understanding their chat data before the call and also reading through that PDF to get a decent prompt. With Deloitte load today it would be ideal if we can push out. (edited) 
Nipuna  [5:35 PM]
@dubois if you want to confirm with them and lmk I can move the meeting ^
dubois  [5:52 PM]
Ok to move to thursday? 
Stephen  [10:31 AM]
@fayaz this is a new metadata file for the conversations.
I've quieried with Ata it has 47k rows rather than 31k there may be something wrong with the join he's done for the new data.
Could you try enriching the 2k conversations with it and seeing whether there are issues with the new rows, or wether this adds the new fields successfully.

Nipuna  [4:10 PM]
@Stephen Whats the plan for Nesto? Gemini issue still isn't sorted to make any progress today.
I also think Max/Ben (sales) might be also both out on vacation for the Tuesday 3rd meeting.
Should we still have the sync on Tuesday to check with Karim and Ata to discuss what we can do?[4:10 PM]Other alternate solution: Is it possible to edit a config value for the Gemini API call to just use the default safety filter for now? If possible we can ask Ata to adjust some backend config? Some calls might fail but assuming we can at least get results.
dubois  [4:13 PM]
Nesto recently acquired a company that is full Azure
[4:13 PM]and they might be able to bring in their OpenAI keys, working with Karim on that in parallel
[4:14 PM]Karim is really fed up with Google bullshit… getting access to API seems to be the most basic thing
Stephen  [12:45 PM]
This is the file from Max, Nipuna chased Ata last Wed on Gemini/Claude, I've followed up for today.
Call today at 19:00 will be a bust as we don't have any time to do any work even if they turn up with access today.PDF


dubois  [4:02 PM]
@Nipuna @Stephen can we have a quick sync on deliverables and plan for nesto?
Stephen  [4:03 PM]
Nipuna just joining a trouble shooting call now I think for Definity - I can talk https://us02web.zoom.us/j/4285614273?pwd=Y1hpNjVuK0k3bS8wZi9yYmpGdUhXQT09
Nipuna  [11:31 PM]
Dropping some progress on Nesto. Been working most of the day to ensure the prompt is accurate and meets the nuances in these calls. Final prompt in the workspace (SDR calls) HERE called (Script Compliance Prompt - v3 (CompareMortgages)) .

Created a test set of 11 convos with different end outcomes and after a 4 iterations happy with prompt and results. The only hickups seem to be due to mis-transcriptions or bad recording. The test set file will show those with the notes.

"v3_final_test_set.xlsx" --  test set file with annotations and notes
"v4_full_pipeline_pivot_268.xlsx" -- pivot of pipeline result across all 268 calls. can individually filter by agent

Data Annotated Workspace CompareMortgages-Script_Compliance (all the prompt results are attached back as metadata -- look for crtieraX_name). Can filter by score or agent direct in this workspace: LINK HERE

Draft Deck (WIP): https://docs.google.com/presentation/d/1RyYhf6y3ApRgGiGDZbexGKzf_h3nqEJPlesgzKsJOCk/edit?usp=sharing

Next Steps:

Add more convos from the test set as examples on slide deck
Some form of insight on best agent / worst agent
Probably focus on the most active agents in the campaign since some have like one calls
Advice column seems very broad and less useful but the correct actions and incorrect actions are good
Merge Stash prompt TBD on these ^


Deck really shaping up.  I like the individual bars along side coaching.  
Nipuna  [6:13 PM]
Thanks. When do you want to have a run through pre-call?
dubois  [6:25 PM]
do you feel that the coaching tips are a bit underwhelming? not our fault of course, but I feel they could eventually get way more granular on what they track and evaluate SDRs on.
Nipuna  [6:38 PM]
yeah I mean all that output just comes from the correct actions / incorrect actions analyzed on those 4 criteria purely related to "how well SDR followed the script". Working with the only doc they gave us of verbatim scripts.
[6:39 PM]so for sure if they can give like tangible guidelines for specific criteria they want to see under other dimensions (other than script adherance) we can deliver but we need that from them
dubois  [6:39 PM]
yeah exactly so i can communicate that early in the call so that Max understands that our tool gives him the ability to go beyond script adherence
Stephen  [7:38 PM]
Yep let me try and be on a bit early.  Could we add a slide ahead of the first one with a snippet of the SOW objective as a place holder and a big 3 days...

Let Alex recap on contract where we are up to - have the section from the scope.

Then on the next size recap - what we were looking at is script adherence.  Now we can look at much more general things, but you're giving a prescriptive thing and this is what is not happening.

We might want to move the insights up to the top, the charts - this is a view across your entire staff - now lets look at coaching.  Push all the detail to behind a fold, and go over if they want.
[7:41 PM]https://us02web.zoom.us/j/4285614273?pwd=Y1hpNjVuK0k3bS8wZi9yYmpGdUhXQT09
[7:41 PM]Opened this
Stephen  [8:57 PM]
Ok I think that was an amazing level of turnaround of requests and insight in 3 days @Nipuna great job.
https://docs.google.com/presentation/d/1RyYhf6y3ApRgGiGDZbexGKzf_h3nqEJPlesgzKsJOCk/edit?usp=sharing

Max got it, we hit what he wanted to see - snippets - full call analysis - following the guidance.
They really kept getting tripped up on trusting the transcription and really wanted to hear the calls as a fall back.
Tough crowd - want to go fast, want to have something new - but then want it to be totally perfect all the way down.
I worry about their tolerance for the results in tool - filtering etc - really I think they need to get their results out elsewhere and trust what's created.

Actions
Nipuna: send deck
Stephen: check deep link call playback from GCP
Nipuna: Brian Ben 1:1 get in tool - Alex Montreal angle?
Fayaz:  need retranscription on Advanced mode with names per call for 268 Compare Mortgages.
Reload data with deep hyperlink
Setup session next week to do playbacks in English and French (edited)


eah I think Max took it well and had the "Aha" that they could run this across and get insights really fast.

I also think the call transcript issue just matters for just that single criteria of introduction so agree Ben was getting tripped up. He was worried about the single example vs overall the advice he can give very quickly if he just spent 10 mins per agent in that table view.

On Actions:

Will send out the deck
The 268 calls ids for CompareMortgages is in the CSV. The campaign_nm should equal these:
Compare Mortgage Leads - EN
Compare Mortgage Leads - FR
Compare Mortgages inbounds - bilingual
I've also split the emails into first name last name for the agents in that 268 (seperate CSV) to make it easier for Fayaz
On a separate note can we also try to get the success_ind field with this new data from BQ after transcription
Ata raised this here
This field sdr_to_adv_success_ind wasn't in the current dataset so need to pull from BQ for those convoIDS as its the final field that denotes if a call was successful transferred to advisor
This helps build on the use case Max mentioned of comparing how does the grading correlate to success or not in real metric. Think it will be really useful to show next week.

Next Tuesday Verizon conflicts so let me try to move them up by 30m so we have the full 2-3pm EST slot (will send invites after)
To get them on tool, Ata needs to invite -- need to work out how keycloack pass through would work for them with Ata or Marc

So just comparing using a prompt to fix transcription vs new transcription with metadata, I think the prompt might be better (in terms of getting a cleaner output). I used Claude to mostly ONLY identify & fix mistranscriptions with the agent names and not touch anything else.

Given that I'm relying on the LLM to give me the conversation back and pre-process back into HF, it does sometimes miss / combine or remove a unclear utterance as seen in one of the examples.

Out of 268 convos, this happened to 3 convos where (1-2 utterances were removed or combined). Rest 265 are all the same input length. But overall given that this fixes the issue, I think best to stick with the prompt results vs new transcription. (edited)

Mapped the SDR total success transfers % onto the chart (darker line). Shows if outbound call transferred to Nesto advisor or not. Green line is total count of calls dialled. Dataset is of the prompt transcription fixed convos.

With the Agent Name transcription fixes, the scoring/ranking has slightly changed around for few agents positively
With this you can see things like given the number of dials, script adherence score, and successful transfers -- Alexandre is one of the best agent overall
Feeds into what Max wanted to see how scores / analysis translates to tangible conversions


Success to transfer is obviously dependant on a lot more than script adherence like lead eligibility ect. With this indicator maybe we can find more insights on what led to successful transferred calls  (reason's for why calls where the lead was eligible didn't get transferred to agent, objections that came up/what did agent say that was different to less vs more successful calls).

Overall in a good place for Tuesday to review the previous set with fixes. Ata gave access to bucket and confirmed direct links to audio is working! All the data has been annotated in this workspace (url field, sdr success, new scores) and slowly updating deck. (edited)

Uploaded both enhanced and standard transcriptions with correct call_ids. nesto_268_calls_enhanced_output  is transcription with enhanced accuracy and nesto_268_calls_output is transcription with standard accuracy.

Standard transcriptions are here - https://humanfirst.nesto.ca/playbooks/playbook-P7PN34KW3FAL5MOCSRNKKFO6/explore/uttera[…]TabId=data-938a97af-0c42-408c-a522-be061dd4b057&matchType=0
Enhanced transcriptions are here - https://humanfirst.nesto.ca/playbooks/playbook-I42RJT5UFFGGPHAI7YI7FDPB/explore/uttera[…]TabId=data-cadacbe6-2ccf-4c2a-af7f-f93279f12b88&matchType=0

I could see overall the English transcriptions correctly identifying the agent names whereas the French one struggling in the standard accuracy transcription.

The enhanced version seem to give better results but still need to do deep dive and make a thorough checking. @Nipuna I'll leave this you.
Here is an example comparing standard and enhanced versions - Session_id: 0723FE4459094986929149E49EE31329. Agent name is Hosanna. Standard detects as Susanna whereas Enhanced detects it correctly as Hosanna. (edited)


eplied to a thread:One note, the newer transcriptions change Compare Mortgages to Compare Mortgage Leads on some calls which throws off the grading prompt. The SDRs would never mention the "Leads" part since their pretending to be calling from CompareMortgages. Wondering if the "Leads" part was included in the content enrichment by accident?

I'm trying to loosen the grading prompt to get around that as a mis-transcription but just something to check for next time.image.png

Ok so overall I've gone ahead and updated the scoring prompt, re-ran on the dataset, highlighted the improvements, finished examples on the deck. Updated Deck + Workspace

Didn't have enough time to generate end-to-end insights on the scores themselves so today will mostly be a sync on the improvements to the transcription. Overall the Advanced mode seems to be working much better and the overall scores have jumped postively.

I left the prompt transcription improvement option as an optional if they want to fix the bad quality audio files "forcefully"


Things to sync on with Max/Ben:

Whats the best format to give these numbers to SDRs? PDF per SDR / CSV?
What are the criteria that SDR use determine if a lead was eligible or not? --> Helps us find the calls with eligible leads and compare whos not convering those and why.
(edited)

Great stuff both let’s show what we can.  Thank you!
Stephen  [8:46 PM]
Rough:

Crawl Walk Run is per campaign - being able to adapt the transcript and be able to see the.
Script adhereance - channel acquisiton - paid search.
Log in time - not needed - ratio calls v handed over.
End of the week Brian end of the week.

Compare Mortgages - pivot tomorrow
Highlight the ones do and dont' let them mark up.
Outbound only

Ata 2023-2024 - use the existing validation - brian white.
Permission for table and schema

Come back delivery time line

@dubois I can see meeting today 18:00 GMT, 13:00 EST - I'm going to have to be on a train during that time coming back from Ebay/Yell.   I can try and join - but signal is patchy on that part of the line I'm likely to be on.

We are waiting for nesto to come back with campaigns.  I have sent data.
We then need to rewrite the pipeline to individually feed the call metadata per transcription (i.e only one agent name only the right campaign names) - we cludged it for the 268 to get timelines.
We have not planned this yet and next week is busy - we are cancelling next week Tuesday meeting as we won't have any progress.  Say 1-2 weeks around other things.
We will then have data - next steps is working out export back into BigQuery - we can write this and Ata will give us priviledges to do.  Say another 1-2 weeks around other things.
Then we will need to start on some basic visualisations.

Nipuna Peiris
Fri, Sep 27, 3:12 PM (3 days ago)
to Max, me, Brandon, Alex, Ata, ben, Karim

Hi Max,

Hope you're well, thanks for the response! Just have some quick questions to get things rolling.

Q1: Going off what you said above, are these the ones we're interested in? Total 16 campaigns.

Q2: In the script document provided, there is a script for 1st Dial Leads and Nth dial leads. It has an introduction message and mentions "Pivot to Flow". Is there more of a flow they are expected to follow? 

From reading a few calls, it seems the process is the same as CompareMortgages going Introduction --> Understand User Situation --> Validate Eligibility (Credit Score, Salary) --> Clear Next Steps (Transfer, Callback).
If there's any further guidance documents, please let me know so I can include that in the prompt. The current doc includes only the following:

1. Campaign: 1st Dial Leads – these have voicemails -- ENGLISH
Call: Hi this is (SDR NAME) from nesto mortgages, calling about the inquiry you made on our website. I’m going to collect a few important details and have you speak with an expert mortgage advisor so they can help you lock in a great rate for your home. (Pivot to Flow)
Voicemail: Hello (CLIENT NAME) This is (SDR NAME) from nesto mortgages. I am calling in response to your inquiry about locking in these low rates. Call me back at 1 877 405 1514. I am here till 6 pm. Again this is (SDR NAME) from nesto calling you about your (renewal/purchase). I am excited to help you lock in the low rates on your mortgage, call me back at 1 877 405 1514 before 6 pm EST.


Stephen  [3:04 PM]
how will the API work on Nesto on prem - depends on SDK refactor.
stephen: Raise with Fayaz and Marc
nipuna: work on ABCD/prod for first tests.

python script to do sync HF to BigQuery
nipuna: going to try on existing ABCD work based on Definity/existing SDK/ just working it out.
Assumption is manually run for version 0.
Use normally academy template (or as jupyter notebook with a function accepting the variables)
Assumption is an upsert for version 0, i.e whole pipeline is synced to the whole table.
Therefore columns are not imporant only the original call_id.  I.e pipeline could prodce 5 columns run 1 and 8 run 6 and whole table is updated - what to do on hallucination.
(explore - what if hallucinates columns)

accepts namespace, workspace, pipeline, creds as env variables using SDK, target table in GCP creds as GCP library
explore gcp bigquery library


revisit inserting BQ schema
Stephen: explain to Fayaz tomorrow and get to resummarise for when nipuan coming to.
- csv v json upload to bigquery
- auto detect v manually define schema
avoid hard coding into the document.
data may already be present.
so use an upsert as a starting point.

Then do joins
table_1 is source input data (already exists)
table_2 is pipeline output (variable columns based on pipeline output)
common key - "call_id"
join_1 onto 2
for aggregation create a view over the top.
looker studio sits on the view.

Sample size
total population ~ 3000
sample should be
at 80% confidence with 10% margin of error - 41 necceary
16 agents
at least 3 calls from each agent.
spreadsheet.
text file
stephen: produce TDD blindset for filling out.

Eval grading
oliver: do on blind.
only grade the 0 1s
done by a human in site of the prompt - because that determines loose ness.
with the conversation.
but with no idae of otput.
reload in with post_fixes column_name_gtruth
upload into tool with tag for testset
run pipeline filtering for testset
get columns up
and compare. (edited) 
Stephen  [4:42 PM]
@Nipuna could you attach here the latest prompt for oliver as a TXT file?
Nipuna  [4:46 PM]
Yea here it is + the document prompt its based on.
2 files SCRIPT_ADHERANCE_V5.txtPlain TextSDR Scripting Campaign for Ben to fill out.pdfPDFStephen  [5:26 PM]
@oliver here is the XLSX with the sampling done.
I tried to lay it out in a sensible way which was harder than I thought it was.
I find them quite hard to read in this format
There are also French calls - I'd suggest skip them and we'll get a native speaker to do, concentrate on the English and the process.
update the xlsx as you best think - really trying to work out a method here.


@Marc Alloul @fayaz so raising this after having talked through a bit with Fayaz.
how does a dev with the SDK in a Jupyter Notebook or a Python script - connect to the Base URL with Creds to the nesto environment.
I.e the new SDK has parameters to pass these, but how is the actual process of connecting done - do we expose the API end point, do we have some sort of additional security layer etc?Stephen  [10:54 AM]
Permission issues with list GCP buckets
Testing on informcomm four files and the HF bucket - Fayaz see if you can add for yourself the permissions you need.
Getting an explicit list of needed permissions to work useful because then can give exactly and only what we need to a third party like nesto.
https://console.cloud.google.com/iam-admin/iam?project=unified-skein-357013
accounts.google.comGoogle Cloud PlatformGoogle Cloud Platform lets you build, deploy, and scale applications, websites, and services on the same infrastructure as Google.Stephen  [12:39 PM]
@oliver spotted that the XSLX only has client utterances (because downloaded from data pane)
I tried to do via ./zia from convoset which normally the way to get both - hard because nesto is on prem.
All felt like going in the wrong direction, so have zagged a bit.
Here is now a dedicated workspace in nesto on prem which is much nicer way to view the calls.

the prompt is there for eval
there are no generated results
The first utterance of every call has a metadata label "is_sample" Y|N
For the 41 test calls, I've turned that into a tag "is_sample"
So if you filter for that you get the 41 test calls and can click through
there is no obvious way to then give the 4 values for each call, so back in the spreadsheet probably the way right now.
https://humanfirst.nesto.ca/playbooks/playbook-BBOHQKMAWNHUXEJQKPUHHIT2/explore/uttera[…]J6JUCHSBI&tagQuery=tag%3A%28tag-27GXYWKNJBA7PFYMUMI5D4ZH%29

To login to nesto reminder that have to login to 1Password find Nesto humanfirst-admin which will let you through the first SSO and then get in.


~~50/50 some agents only have en or fr calls so it was an approx based on covering the agents in the language they speak.
oliver  [2:47 PM]
ok so the first criteria was relatively easy to mark, 2 and 3 are proving more challenging
[2:48 PM]there are requirements that are either implicit or dificult to evidence in a call transcript
[2:51 PM]When validating eligibility there are two paths the Agent can take. If the Agent determines the User is not meeting the requirements they do not need to validate credit, postal code or other details. If the Agent determines User did meet basic requirements, they are to properly validate eligibility. Note that the Agents may have some context on the type of mortgage application the User is inquiring about prior to the call.

"Perfect! I can definitely have a couple of our partners reach out to you, once I confirm a few simple details: Are you looking to renew, purchase or refinance a home? How would you rate your credit fair, good, excellent, and What is the postal code for the home?" 
- Expectation: Here the agent is to validate the customers eligibility before transitioning to the mortgage advisor.
- Score: Give score of 1 if the agent attempted to validate eligibility using a few questions. Give score of 0 if the Agent didn't make any attempts to validate User's before transfering. Respond "unclear" if it cannot be determined. Respond "no_need_to_validate" if the User doesn't meet the basic requirements.


How do I know if the agent determines the user is not meeting the requirements?
What does properly validate eligibility actually mean?
[2:53 PM]which then makes criteria 4 difficult to do as it relies on knowing if the user is eligible
Stephen  [2:55 PM]

How do I know if the agent determines the user is not meeting the requirements?
If they are not offered a handover to a broker at then they didn't meet the requirements.
What does properly validate eligibility actually mean?Yes this hard - most agent do this well as they are following a screen which has the requirements on - but we as HF haven't ever seen.  Over a few calls you'll see the sort of thing asked for like - when are they thinking of taking the mortgage, what their salary is, whether they know their credit rating.
oliver  [2:56 PM]
If they are not offered a handover could also mean that the agent failed to follow the proper procedure?
Stephen  [2:56 PM]
The bot also doesn't know this so I would fall back for two on the core rule guidance
 Give score of 1 if the agent allowed the User to explain their situation and understood them. Give score of 0 if the Agent didn't make any attempts to understand the User's current situation. Respond "unclear" if it cannot be determined.[2:57 PM]If they are not offered a handover could also mean that the agent failed to follow the proper procedure?If the agent didn't ask them any questions, then yes.  But if they asked what look like suitable eligibility questions and then didn't get to a handover this is fine.  Followed procedure, customer just not eligible.
oliver  [2:58 PM]
it feels a bit wishy washy on their part to me but will attempt to follow
[3:00 PM]and what you just explained to me feels like it should be part of the prompt
Stephen  [3:00 PM]
Yeah - if you look at the guidance we have - it's literaly that 1 page of training in the PDF - so nipuna's tried to find some core hard criteria from that to evaluate.  Without looking at the results - @Nipuna you got some time to take @oliver through the guidance and the prompt?   Also can we check the prompt between criteria 3 and criteria 4 - there might be some cut and paste error.
[3:01 PM]But also this is just good prompt feedback, and exactly what we should be doing - the TDD process guiding the evolution of the prompt.

We had to through this prompt together to get to a meeting with about 1 day notice because of the difficulty getting to everything in the on prem environment the way nesto wanted - spending some time thinking and clarifiying now as a team will pay u sback.
Nipuna  [3:07 PM]
@oliver happy to sync around 9:30am EST. Have to send out the course invites right now.

What does properly validate eligibility actually mean?Validate eligibility is purposefully vague since they didn't give us a list of things that an Agent actually checks. Generally the prompt will give a 1 if they asked some questions to check credit score / mortgage renewal or new purchase ect. Its very loose b/c some agents ask 1/2 questions, some ask all the questions and some don't ask any. The idea is to just give 0's only if they don't even attempt.

For next steps part -- again I changed to "next steps" instead of "handover" b/c of the above.
Its defined next steps b/c its quite uncertain what makes someone eligible / not (seems to be things like if renewal is in 120 days ect)
Also according to Ben sometimes Agents won't even transfer to a advisor even if valid b/c advisors aren't available. So next steps is vague to just give a 1 if they set up some sort of clear direction as a transfer or as a callback from a partner bank.


Nipuna  [4:00 PM]
@fayaz thanks for the quick turn around! So I reviewed most calls. Majority are spot on (I would say ~85-90%). The website names were recognized pretty much every time.

The only issues I noticed were with Nav and Kyle. I added a bit more examples for both to see if it would help pick up in the new file. Kyle tends to pronounce his name as "Carl" possibly due to french accent but I added some more enrichment for both. Overall I think thats the extent of what we can do given their audio quality.

Other notes:

Two convos were missing agent_id and call_id fields but had session_id only (BQ pulldown CSV seems to have the info so perhaps it didn't get mapped correctly? )


OK Max and Ben out, Karim and a last minute addition Sukhman Grewel on from commercial side.
Request from Karim is "can we spend some time Friday onboarding Sukham so he can investigate some PxD use cases and how will the billing work" @dubois said I'd check with you, but we've booked the time Friday.
Use cases sound like reviewing one document for risk against another document which contains the guidance for risk assessment.
Asked what type of document, seemed to be likely to be long form PDFs, have said that upload isn't available right now, but we can convert a test data set for them, and it's coming shortly.
Things seemed to be moving positively - but wanted to check where negotiating was on move forward without saying no.


Walkthough Call w/ Sukhman -- Oct 11

He's part of Intellifi (~800 ppl) firm supporting specifically regarding commercial mortgages (CMs) in Canada. Recently bought by Nesto.
A large focus of the use case he's exploring is around document parsing and then extraction:
Big pain point is different documents in CMs across providers aren't uniform (Rent rolls, operating statements, contracts ect)
Lots of table data or images in a PDF document

The hardest part regardless of whatever LLM app they use is going to be the data parsing side of getting the data out of the PDF in a structured format to be used for an LLM
Tons of document parsing libraries out so mentioned we can support with this if needed



Tool Overview

Walked through the tool / prompts / pipelines with Clinton emails
Asked a good amount of questions and was suprised how easy it was to run across a 1000 things
Showed immediate clustering / metadata key value extraction
He mentioned they would need it in JSON as they need the extracted object to have a lot of nested arrays, dicts ect


Overall he sees a few use cases other than the document one on the chat side as well. Interested in automated pipelines via an API. Data segregation was an important topic (they need to be in Canada - mentioned thats not really an issue since Nesto is on-prem regardless). They're only mostly comfortable with using Gemini as Google promises that.

Next Steps

Wants to try the tool and then reach out
Asked him to get Karim/Ata to invite to combined Slack channel (he still doesn't know most of the Nesto team)
Once he joins prob will need to get him access to Nesto instance
(edited)

Recap last week

need to simplify prompt
evaluation criteria as yes/no able
rerun on 3000


eally good insights.

I suggest we use the golden set against the first prompt version, baseline that result, then do a second one codifying guidance on these to see if that improves

Notes on how might do that.

0/1 - we were experimenting without an unclear because if it's specific enough I feel like it shouldn't be necessary and the default as you've done in a 0.  I.e call is a voicemail and therefore that should be in the reasoning?  May still be worth being explicit with the prompt for this.

On the website is in the instruction - interesting to see if that (correct) assumption you made is matched by LLM without guidance.  Otherwise I think we bracked guidance after in the same section to keep it still really tight and focused and reusable in a human questioning format for test results.

reason_for_call: Did the Agent mention the reason for calling is regarding an inquiry started on the website? (it is necessary to mention the source of the inquiry)"

Maybe the wording on the verify questions is better as:

"Was the Agent able to establish... "

mortgage_need: Was the Agent able to establish why the User needed a mortgage?
mortgage_timeframe: Was the Agent able to establish the User's likely timeframe for getting a mortgage?

Which makes it clearer that if it's implicitly mentioned then it's OK.

There is also a question here about whether we need and "if" in the logic and separate the 8 up into two parts.

I.e start of call - definitively should happen.  Then if the call is progressing are they able to establish the following information

timeline
creditscore


Then an if for the two roots out of a call.

Really depends on what we are grading.  If we are grading the call just as a call (rather than adherance) then giving 0s when info is bad is fine.  I.e if it's a voice mail that's fine because that call/time is unproductive which shows up with the 0s, but it's not necessarily a reflection of the agent ability.

Then in the second pass and prompt the agent quality can be looked at for coaching by comparing the 0/1 scores with the reasoning and giving it guidance to be forgiving on calls where it wasn't possible to do the things and concentrate on common patterns where the agent could have improved.


Made some good progress on Nesto:

BQ Delete then Insert script modification done
Ata granted permissions to my email so created insight_table and used script to insert local HF JSON of 3.6K calls (local since on-prem) -- BQ LINK
Had to use gcloud CLI to auth since I can't create Service Accounts on their project. Good for now but can ask later for a separate service account credentials.

Created two views - waiting on Ata to share with connection to Looker Studio report
One view is the raw call data joined onto insights table metrics (vw_insights_join) 
Other view aggregates the avg total scores across agent/campaign nm (vw_agent_stats) 

Replicated this entire process on ABCD too with 3k calls and built a sample dashboard on our GCP
Link here

Stephen  [10:34 AM]
We also need to do the next prompt on the output of this onto the conversation for the coaching conversation.
I think something like a simpler looker layout with the individual charts and some way to browse a table of coaching snippets and links back into the tool.Stephen  [1:04 PM]
Key Nesto dates:
2024-06-03 pre-project on-prem design and delivery starts.
2024-08-12 on prem available and kickoff held but only with text-bison available - we have only 48h to produce anything using only text-bison because of previous delay.  Client not happy with results.  Now blocked by lack of Gemini in Nesto
2024-09-03 Having been frustrated by Google Gemini - Nesto finally makes Anthropic available on their GCP and PS work starts for real.
2024-09-10 We produce first analysis recapturing client confidence, but we are rushing into each with compressed time from the above.  Becomes clear client wants snippet level information audio playback
2024-10-27 We have snippet level analysis and a now very complicated approach that turns loose PDF guidance into something meaningful at a level the client trusts.  But it's clear they could not use or maintain something of this complexity.
2024-10-08 Max leaves and we use as an opporuntity time to refactor the core approach and prompts to produce something useful for internal usage on how to understand and implemnent evals, and to manage client understanding of the "rules" section of CIDER prompts.
2024-10-12 Start onboarding completely new person for new PxD Analytics use cases - Sukham

Current status
Have visualisations runnning on ABCD in looker based on an a draft HF -> BQ incremental update archiecture.  3000 calls all transcribed at snippet level.
Refactored the core analysis prompt and upped quality from initial ~50% agreemnt, through 84% to now ~92% human to AI agreement.
Need to complete a second prompt, which operates on the output of the first to produce the desired individual level coaching report.
This will need a second dashboard producing.


Stephen  [6:00 AM]
Trying to think about how that would work

need to workout if looker supports a hover value or click link on the segments 
filters in HF can be deep linked into (take the URL from GUI and update the params basically
if looked supports it then Its a case then of working out for each visual what link to assemble makes sense
For too left chart it would metadata = agent email  and metadata = resolved or not which should be assemble into a unique link for the two parts of the chart


Stephen  [12:06 PM]
Thanks @Nipuna this looks great.  Lets separtely think on the security implications just so we don't bump accidentially into anything.
Hi Karim,

I have shared access to the initial Looker Dashboard that is currently in development for the POC regarding analyzing SDR outbound sales calls. There are a few more pieces we're working on finishing up but here is the current draft:

https://lookerstudio.google.com/reporting/da5cc602-36e3-4adc-b9de-68b0fdb45882

It provides call guidance stats across 8 different criteria for each agent. There are currently around ~3,600 calls processed and visible on the dashboard plus aggregated stats per agent for CompareMortgages Campaigns. 

The data is already uploaded and present in Nesto's BQ project shared by Ata. There is a separate Page to click directly into HumanFirst for deeper insights and to review the conversations directly.

Could we arrange the session later this week for a walk through either Thur Oct 31st 12:00pm-1:00pm EST this week or we have a recurring slot next week on Tuesday Nov 5th 2:00pm-3:00pm? Let me know if any of those work, thanks!

Nesto Status:

Email sent to Karim and access granted to team
Tool tips added to describe each criteria in dashboard on hover as he requested (table only)

Followed up with Ata yesterday on Looker access (he's going to reach out to security team again):
Ata Teimoori  [10:44 AM]
I'm still waiting for the security team
let me follow up with them


Deck for walk through of whole process / project for likely next Tuesday meeting (Karim hasn't confirmed date but prepping in advance) -- HERE



Call guidance merge stash prompt started (WIP)
This prompt to run on generated scores to produce a summary / report
Got a basic version working HERE producing good results but shifting gears to focus on Zapier
Still need to ideate how this fits into dashboard


Nesto Technical Handover Session (Ata / Marnix / Nipuna)

Overall great session - walked through a end to end example of the manual process
100 calls CSV -> upload to tool -> setup prompts/pipelines -> download as JSON -> push up to sample BQ table
covered basics of HF formats, data uploads, where data sits ect.

Did the manual step through for this call to help familiarize with UI. They are both very technical so keen on looking at automating which I mentioned can be done via SDK and API. TBD need a separate call since some stuff needs to be worked out.


Transcription

They had some transcription questions that I couldn't quite answer but walked through the scripts as a whole
Does speechmatics use the two channels to identify roles? 
Marnix noted that speechmatics supports diarization as well 

How does the URL click through to audio field get mapped from the raw data? Where does it get the session_id from?
Saw on the call that the speechmatics-to-hf-csv script there was a url field being constructed but didn't know where the actual metadata came from whether its from the file name of the call or whatever

@fayaz can you please drop Ata a message on these questions. If you can shoot a 5 min loom on how the transcription part was done for Nesto from GCP bucket to HF CSV and drop it in the external channel it would really help. Mentioned I'll check with you and follow up. ^



Actions

 (DONE) Email Ata all relevant docs/transcribed calls/content enrichment
Follow up with Ata on transcription questions above
Ata to get Marnix added to IAM GCP so he can access the tool
Going to need to figure out how to expose on-prem HTTP endpoint URL so we can point SDK to that
@Marc Alloul when you have a chance can you write up a guide or commands to do this ^

Finish Airflow Example