DROP DATABASE IF EXISTS clinical_trials;
CREATE DATABASE clinical_trials CHARACTER SET = 'utf8';

USE clinical_trials;

DROP TABLE IF EXISTS ct_results_events_other_counts;
DROP TABLE IF EXISTS ct_results_events_other_events;
DROP TABLE IF EXISTS ct_results_events_other_categories;
DROP TABLE IF EXISTS ct_results_events_other;
DROP TABLE IF EXISTS ct_results_events_serious_counts;
DROP TABLE IF EXISTS ct_results_events_serious_events;
DROP TABLE IF EXISTS ct_results_events_serious_categories;
DROP TABLE IF EXISTS ct_results_events_serious;
DROP TABLE IF EXISTS ct_results_events_groups;
DROP TABLE IF EXISTS ct_results_analysis_groups;
DROP TABLE IF EXISTS ct_results_analysis;
DROP TABLE IF EXISTS ct_results_outcome_measure_values;
DROP TABLE IF EXISTS ct_results_outcome_measure_categories;
DROP TABLE IF EXISTS ct_results_outcome_measures;
DROP TABLE IF EXISTS ct_results_outcome_groups;
DROP TABLE IF EXISTS ct_results_outcomes;
DROP TABLE IF EXISTS ct_results_baseline_measure_values;
DROP TABLE IF EXISTS ct_results_baseline_measure_categories;
DROP TABLE IF EXISTS ct_results_baseline_measures;
DROP TABLE IF EXISTS ct_results_baseline_groups;
DROP TABLE IF EXISTS ct_results_periods_drops_participants;
DROP TABLE IF EXISTS ct_results_periods_drops;
DROP TABLE IF EXISTS ct_results_periods_participants;
DROP TABLE IF EXISTS ct_results_periods_milestones;
DROP TABLE IF EXISTS ct_results_periods;
DROP TABLE IF EXISTS ct_results_groups;
DROP TABLE IF EXISTS ct_results;
DROP TABLE IF EXISTS ct_browse_intervention;
DROP TABLE IF EXISTS ct_browse_condition;
DROP TABLE IF EXISTS ct_keywords;
DROP TABLE IF EXISTS ct_responsible_party;
DROP TABLE IF EXISTS ct_results_references;
DROP TABLE IF EXISTS ct_references;
DROP TABLE IF EXISTS ct_links;
DROP TABLE IF EXISTS ct_removed_countries;
DROP TABLE IF EXISTS ct_countries;
DROP TABLE IF EXISTS ct_location_investigators;
DROP TABLE IF EXISTS ct_locations;
DROP TABLE IF EXISTS ct_overall_officials;
DROP TABLE IF EXISTS ct_interventions_other_names;
DROP TABLE IF EXISTS ct_interventions_arm_groups;
DROP TABLE IF EXISTS ct_interventions;
DROP TABLE IF EXISTS ct_arm_groups;
DROP TABLE IF EXISTS ct_conditions;
DROP TABLE IF EXISTS ct_other_outcomes;
DROP TABLE IF EXISTS ct_secondary_outcomes;
DROP TABLE IF EXISTS ct_primary_outcomes;
DROP TABLE IF EXISTS ct_oversight_authorities;
DROP TABLE IF EXISTS ct_collaborators;
DROP TABLE IF EXISTS ct_lead_sponsors;
DROP TABLE IF EXISTS ct_secondary_ids;
DROP TABLE IF EXISTS ct_nct_aliases;
DROP TABLE IF EXISTS ct_master;

CREATE TABLE ct_master (
	id varchar(15) NOT NULL PRIMARY KEY COMMENT 'NCT Record ID (internal primary key)', 
	download_date VARCHAR(100) COMMENT 'Date record downloaded from CT.gov',
	source_url VARCHAR(100) NOT NULL COMMENT 'URL For source NCT record',
	org_study_id VARCHAR(100) COMMENT 'Unique protocol ID assigned by sponsoring organization',
	brief_title VARCHAR(1000) COMMENT 'Protocol title intended for the lay public',
	acronym VARCHAR(100) COMMENT 'Acronym or initials used to identify this study',
	official_title VARCHAR(1000) COMMENT 'Official name of the protocol provided by the study principal investigator or sponsor.',
	source VARCHAR(1000) COMMENT 'Information provider',
	has_dmc VARCHAR(10) COMMENT 'Indicate whether a data monitoring committee has been appointed for this study.',
	brief_summary VARCHAR(1000) COMMENT 'Short description of the protocol intended for the lay public. Include a brief statement of the study hypothesis.',
	detailed_description VARCHAR(1000) COMMENT 'Extended description of the protocol, including more technical information',
	overall_status VARCHAR(1000) COMMENT 'Overall accrual activity for the protocol.',
	why_stopped VARCHAR(1000) COMMENT 'For suspended, terminated or withdrawn studies, provide a brief explanation of why the study has been halted or terminated.',
	start_date VARCHAR(20) COMMENT  'Date that enrollment to the protocol begins.',
	completion_date_type VARCHAR(20) COMMENT 'Final date on which data was (or is expected to be) collected.',
	completion_date VARCHAR(20) COMMENT  'Anticipated or Actual',
	primary_completion_date_type VARCHAR(20) COMMENT 'As specified in US Public Law 110-85, Title VIII, Section 801, with respect to an applicable clinical trial, the date that the final subject was examined or received an intervention for the purposes of fina
l collection of data for the primary outcome, whether the clinical trial concluded according to the prespecified protocol or was terminated.',
        primary_completion_date VARCHAR(20) COMMENT 'Anticipated or Actual',
	phase VARCHAR(10) COMMENT 'Phase of investigation, as defined by the US FDA for trials involving investigational new drugs',
	study_type VARCHAR(100) COMMENT 'Nature of the investigation.',
	study_design VARCHAR(1000) COMMENT 'Primary investigative techniques used in the protocol.',
	target_duration VARCHAR(100) COMMENT 'For Patient Registries, the anticipated time period over which each participant is to be followed.',
	number_of_arms VARCHAR(10) COMMENT 'Number of intervention groups',
	number_of_groups VARCHAR(10) COMMENT 'Number of study groups/cohorts.',
	enrollment_type VARCHAR(10) COMMENT 'Anticipated or Actual',
	enrollment VARCHAR(100) COMMENT 'Number of subjects in the trial.',
	biospec_retention VARCHAR(1000) COMMENT 'Biospecimen retention',
	biospec_desc VARCHAR(1000) COMMENT 'Specify all types of biospecimens to be retained (e.g., whole blood, serum, white cells, urine, tissue).',
	study_pop TEXT COMMENT 'For observational studies only, a description of the population from which the groups or cohorts will be selected',
	sampling_method VARCHAR(1000) COMMENT 'For observational studies only, select Probability or Non-Probability Sample',
	criteria TEXT COMMENT 'Summary criteria for participant selection.',
	gender VARCHAR(10) COMMENT 'Physical gender of individuals who may participate in the protocol.',
	minimum_age VARCHAR(10) COMMENT 'Minimum age of participants.',
	maximum_age VARCHAR(10) COMMENT 'Maximum age of participants.',
	healthy_volunteers VARCHAR(10) COMMENT 'Indicate if persons who have not had the condition(s) being studied or otherwise related conditions or symptoms, as specified in the eligibility requirements, may participate in the study.',
	contact_first_name VARCHAR(100) COMMENT 'First name of person providing centralized, coordinated recruitment information for the entire study.',
	contact_middle_name VARCHAR(100) COMMENT 'Middle name of person providing centralized, coordinated recruitment information for the entire study.',
	contact_last_name VARCHAR(100) COMMENT 'Last name of person providing centralized, coordinated recruitment information for the entire study.',
	contact_degrees VARCHAR(100) COMMENT 'Degrees of person providing centralized, coordinated recruitment information for the entire study.',
	contact_phone VARCHAR(100) COMMENT 'Phone number of person providing centralized, coordinated recruitment information for the entire study.',
	contact_phone_ext VARCHAR(100) COMMENT 'Phone extension of person providing centralized, coordinated recruitment information for the entire study.',
	contact_email VARCHAR(100) COMMENT 'Email of person providing centralized, coordinated recruitment information for the entire study.',
        contact_backup_first_name VARCHAR(100) COMMENT 'First name of backup to person providing centralized, coordinated recruitment information for the entire study.',
        contact_backup_middle_name VARCHAR(100) COMMENT 'Middle name of backup to person providing centralized, coordinated recruitment information for the entire study.',
        contact_backup_last_name VARCHAR(100) COMMENT 'Last name of backup to person providing centralized, coordinated recruitment information for the entire study.',
        contact_backup_degrees VARCHAR(100) COMMENT 'Degrees of backup to person providing centralized, coordinated recruitment information for the entire study.',
        contact_backup_phone VARCHAR(100) COMMENT 'Phone number of backup to person providing centralized, coordinated recruitment information for the entire study.',
        contact_backup_phone_ext VARCHAR(100) COMMENT 'Phone extension of backup to person providing centralized, coordinated recruitment information for the entire study.',
        contact_backup_email VARCHAR(100) COMMENT 'Email of backup to person providing centralized, coordinated recruitment information for the entire study.',
	verification_date VARCHAR(20) COMMENT 'Date the protocol information was last verified.',
	lastchanged_date VARCHAR(20) COMMENT 'Last changed date',
	firstreceived_date VARCHAR(20) COMMENT 'First received date',
	firstreceived_results_date VARCHAR(20) COMMENT 'First received results date',
	is_fda_regulated VARCHAR(10) COMMENT 'Indicate whether this trial includes an intervention subject to US Food and Drug Administration regulation under section 351 of the Public Health Service Act or any of the following sections of the Federal Food, D
rug and Cosmetic Act: 505, 510(k), 515, 520(m), and 522.',
	is_section_801 VARCHAR(10) COMMENT 'If this trial includes an FDA regulated intervention, indicate whether this is an "applicable clinical trial" as defined in US Public Law 110-85, Title VIII, Section 801.',
	duplicate INT DEFAULT 0 COMMENT 'Duplicate Flag for deletion'
) COMMENT 'Clinical Trials core record table';

CREATE TABLE ct_secondary_ids (
	id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
	secondary_id_ctr INT NOT NULL COMMENT 'Sequence of Secondary ID in list (internal primary key)',
	secondary_id_type VARCHAR(1000) COMMENT 'Type of secondary ID',
	secondary_id VARCHAR(1000) COMMENT 'Other identification numbers assigned to the protocol, including unique identifiers from other registries and NIH grant numbers, if applicable.',
	FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
	UNIQUE KEY (id, secondary_id_ctr)
) COMMENT 'Secondary Study Identifiers';

CREATE TABLE ct_nct_aliases (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        nct_alias_ctr INT NOT NULL COMMENT 'Sequence of NCT Alias in list (internal primary key)',
        nct_alias VARCHAR(1000) COMMENT 'NCT Alias',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, nct_alias_ctr)
) COMMENT 'NCT Aliases';

CREATE TABLE ct_lead_sponsors (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        sponsor_ctr INT NOT NULL COMMENT 'Sequence of Lead Sponsor in list (internal primary key)',
        agency VARCHAR(1000) COMMENT 'Name of primary organization that oversees implementation of study and is responsible for data analysis.',
	agency_class VARCHAR(1000) COMMENT 'Type of organization sponsoring the study (NIH, US Fed, Industry, Other)',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, sponsor_ctr)
) COMMENT 'Lead Sponsors';

CREATE TABLE ct_collaborators (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        sponsor_ctr INT NOT NULL COMMENT 'Sequence of Collaborator in list (internal primary key)',
        agency VARCHAR(1000) COMMENT 'Other organizations (if any) providing support, including funding, design, implementation, data analysis and reporting.',
        agency_class VARCHAR(1000) COMMENT 'Type of organization sponsoring the study (NIH, US Fed, Industry, Other)',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, sponsor_ctr)
) COMMENT 'Collaborating Organizations';

CREATE TABLE ct_oversight_authorities (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        authority_ctr INT NOT NULL COMMENT 'Sequence of Oversight Authority in list (internal primary key)',
        authority VARCHAR(1000) COMMENT 'The name of each national or international health organization with authority over the protocol.',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, authority_ctr)
) COMMENT 'Lead Sponsors';

CREATE TABLE ct_primary_outcomes (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        outcome_ctr INT NOT NULL COMMENT 'Sequence of Primary Outcome in list (internal primary key)',
	measure VARCHAR(1000) COMMENT 'Specific key measurement(s) or observation(s) used to measure the effect of experimental variables in a study, or for observational studies, to describe patterns of diseases or traits or associations with exposures, risk
factors or treatment.',
        time_frame VARCHAR(1000) COMMENT 'Time point(s) at which outcome measure is assessed.',
	safety_issue VARCHAR(1000) COMMENT 'Is this outcome measure assessing a safety issue?',
	description VARCHAR(1000) COMMENT 'Additional information about the outcome measure, if needed for clarification.',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, outcome_ctr)
) COMMENT 'Primary Outcomes';

CREATE TABLE ct_secondary_outcomes (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        outcome_ctr INT NOT NULL COMMENT 'Sequence of Secondary Outcome in list (internal primary key)',
        measure VARCHAR(1000) COMMENT 'Secondary measurements that will be used to evaluate the intervention(s) or, for observational studies, that are a focus of the study.',
        time_frame VARCHAR(1000) COMMENT 'Time point(s) at which outcome measure is assessed.',
        safety_issue VARCHAR(1000) COMMENT 'Is this outcome measure assessing a safety issue?',
        description VARCHAR(1000) COMMENT 'Additional information about the outcome measure, if needed for clarification.',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, outcome_ctr)
) COMMENT 'Secondary Outcomes';

CREATE TABLE ct_other_outcomes (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        outcome_ctr INT NOT NULL COMMENT 'Sequence of Other Outcome in list (internal primary key)',
        measure VARCHAR(1000) COMMENT 'Any other measurements, excluding post-hoc measures, that will be used to evaluate the intervention(s) or, for observational studies, that are a focus of the study.',
        time_frame VARCHAR(1000) COMMENT 'Time point(s) at which outcome measure is assessed.',
        safety_issue VARCHAR(1000) COMMENT 'Is this outcome measure assessing a safety issue?',
        description VARCHAR(1000) COMMENT 'Additional information about the outcome measure, if needed for clarification.',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, outcome_ctr)
);

CREATE TABLE ct_conditions (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        condition_ctr INT NOT NULL COMMENT 'Sequence of condition in list (internal primary key)',
        condition_name VARCHAR(1000) COMMENT 'Primary disease or condition being studied, or focus of the study. Diseases or conditions should use the National Library of Medicine''s Medical Subject Headings (MeSH) controlled vocabulary when possible.',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, condition_ctr)
) COMMENT 'Conditions';

CREATE TABLE ct_arm_groups (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        arm_group_ctr INT NOT NULL COMMENT 'Sequence of arm_group in list (internal primary key)',
        arm_group_label VARCHAR(1000) COMMENT 'the short name used to identify the arm.',
	arm_group_type VARCHAR(1000) COMMENT 'type of arm (enumerated list)',
	arm_group_desc VARCHAR(1000) COMMENT 'brief description of the arm.',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, arm_group_ctr)
) COMMENT 'For interventional studies specify the arms, corresponding to Number of Arms specified under Study Design (for single-arm studies, the following data elements are optional).';

CREATE TABLE ct_interventions (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        intervention_ctr INT NOT NULL COMMENT 'Sequence of intervention in list (internal primary key)',
        intervention_type VARCHAR(1000) COMMENT 'type of intervention (enumerated list).',
        intervention_name VARCHAR(1000) COMMENT 'for drugs use generic name; for other types of interventions provide a brief descriptive name.',
        intervention_desc VARCHAR(1000) COMMENT 'cover key details of the intervention. Must be sufficiently detailed to distinguish between arms of a study (e.g., comparison of different dosages of drug) and/or among similar interventions (e.g., comparison of mu
ltiple implantable cardiac defibrillators).',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, intervention_ctr)
) COMMENT 'For all studies, and for expanded access records, specify the associated intervention(s). For interventional studies, at least one intervention must be specified. For observational studies, specify the intervention(s)/exposure(s) of
interest, if any.';

CREATE TABLE ct_interventions_arm_groups (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        intervention_ctr INT NOT NULL COMMENT 'Sequence of intervention in list (internal primary key)',
	arm_group_ctr INT NOT NULL COMMENT 'Sequence of arm_group in list (internal primary key)',
        arm_group_label VARCHAR(1000) COMMENT 'Arm group receiving the intervention',
        FOREIGN KEY (id, intervention_ctr) REFERENCES ct_interventions(id, intervention_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, intervention_ctr, arm_group_ctr)
) COMMENT 'if multiple Arms/Groups have been specified for the study, edit the Cross-Reference, checking boxes to indicate which of the Interventions are to be stered under each Arm/Group of the study.';

CREATE TABLE ct_interventions_other_names (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        intervention_ctr INT NOT NULL COMMENT 'Sequence of intervention in list (internal primary key)',
        other_name_ctr INT NOT NULL COMMENT 'Sequence of other name in list (internal primary key)',
        other_name VARCHAR(1000) COMMENT 'list other names used to identify the intervention, past or present (e.g., brand name for a drug).',
        FOREIGN KEY (id, intervention_ctr) REFERENCES ct_interventions(id, intervention_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, intervention_ctr, other_name_ctr)
) COMMENT 'Other Names for interventions';

CREATE TABLE ct_overall_officials (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        official_ctr INT NOT NULL COMMENT 'Sequence of overall_official in list (internal primary key)',
        first_name VARCHAR(1000) COMMENT 'First name.',
        middle_name VARCHAR(1000) COMMENT 'Middle name.',
        last_name VARCHAR(1000) COMMENT 'Last name.',
	degrees VARCHAR(1000) COMMENT 'Degree(s).',
	role VARCHAR(1000) COMMENT 'Position or function of the official.',
	affiliation VARCHAR(1000) COMMENT 'Full name of the official''s organization. If none, specify Unaffiliated.',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, official_ctr)
) COMMENT 'Person(s) responsible for the overall scientific leadership of the protocol, including study principal investigator.';

CREATE TABLE ct_locations (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        location_ctr INT NOT NULL COMMENT 'Sequence of location in list (internal primary key)',
        location_name VARCHAR(1000) COMMENT 'Full name of the organization where the protocol is being conducted.',
        location_city VARCHAR(1000) COMMENT 'City.',
        location_state VARCHAR(1000) COMMENT 'State.',
        location_zip VARCHAR(1000) COMMENT 'Postal Code.',
        location_country VARCHAR(1000) COMMENT 'Country.',
        location_status VARCHAR(1000) COMMENT 'protocol accrual activity at a facility.',
        contact_first_name VARCHAR(1000) COMMENT 'First name of person providing facility recruitment information for the entire study.',
        contact_middle_name VARCHAR(1000) COMMENT 'Middle name of person providing facility recruitment information for the entire study.',
        contact_last_name VARCHAR(1000) COMMENT 'Last name of person providing facility recruitment information for the entire study.',
        contact_degrees VARCHAR(1000) COMMENT 'Degrees of person providing facility recruitment information for the entire study.',
        contact_phone VARCHAR(1000) COMMENT 'Phone number of person providing facility recruitment information for the entire study.',
        contact_phone_ext VARCHAR(1000) COMMENT 'Phone extension of person providing facility recruitment information for the entire study.',
        contact_email VARCHAR(1000) COMMENT 'Email of person providing facility recruitment information for the entire study.',
        contact_backup_first_name VARCHAR(1000) COMMENT 'First name of backup to person providing facility recruitment information for the entire study.',
        contact_backup_middle_name VARCHAR(1000) COMMENT 'Middle name of backup to person providing facility recruitment information for the entire study.',
        contact_backup_last_name VARCHAR(1000) COMMENT 'Last name of backup to person providing facility recruitment information for the entire study.',
        contact_backup_degrees VARCHAR(1000) COMMENT 'Degrees of backup to person providing facility recruitment information for the entire study.',
        contact_backup_phone VARCHAR(1000) COMMENT 'Phone number of backup to person providing facility recruitment information for the entire study.',
        contact_backup_phone_ext VARCHAR(1000) COMMENT 'Phone extension of backup to person providing facility recruitment information for the entire study.',
        contact_backup_email VARCHAR(1000) COMMENT 'Email of backup to person providing facility recruitment information for the entire study.',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, location_ctr)
) COMMENT 'Locations where protocol is being conducted.';

CREATE TABLE ct_location_investigators (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        location_ctr INT NOT NULL COMMENT 'Sequence of location in list (internal primary key)',
	investigator_ctr INT NOT NULL COMMENT 'Sequence of investigator in list (internal primary key)',
	first_name VARCHAR(1000) COMMENT 'First name.',
        middle_name VARCHAR(1000) COMMENT 'Middle name.',
        last_name VARCHAR(1000) COMMENT 'Last name.',
        degrees VARCHAR(1000) COMMENT 'Degree(s).',
        role VARCHAR(1000) COMMENT 'Position or function of the investigator.',
        affiliation VARCHAR(1000) COMMENT 'Full name of the investigator''s organization. If none, specify Unaffiliated.',
        FOREIGN KEY (id, location_ctr) REFERENCES ct_locations(id, location_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, location_ctr, investigator_ctr)
) COMMENT 'Investigators at the protocol location.';

CREATE TABLE ct_countries (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        country_ctr INT NOT NULL COMMENT 'Sequence of country in list (internal primary key)',
        country VARCHAR(1000) COMMENT 'undocumented',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, country_ctr)
) COMMENT 'Countries where protocol is carried out (?)';

CREATE TABLE ct_removed_countries (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        country_ctr INT NOT NULL COMMENT 'Sequence of country in list (internal primary key)',
        country VARCHAR(1000) COMMENT 'undocumented',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, country_ctr)
) COMMENT 'Countries where protocol has been terminated (?)';

CREATE TABLE ct_links (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        link_ctr INT NOT NULL COMMENT 'Sequence of link in list (internal primary key)',
        url VARCHAR(1000) COMMENT 'complete URL, including http',
	link_desc VARCHAR(1000) COMMENT 'title or brief description of the linked page.',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, link_ctr)
) COMMENT 'A Web site directly relevant to the protocol';

CREATE TABLE ct_references (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        reference_ctr INT NOT NULL COMMENT 'Sequence of reference in list (internal primary key)',
        citation VARCHAR(1000) COMMENT 'bibliographic reference in NLM''s MEDLINE format',
        PMID VARCHAR(1000) COMMENT 'PubMed Unique Identifier (PMID) for the citation in MEDLINE',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, reference_ctr)
) COMMENT 'Citations to publications related to the protocol background';

CREATE TABLE ct_results_references (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        reference_ctr INT NOT NULL COMMENT 'Sequence of reference in list (internal primary key)',
        citation VARCHAR(1000) COMMENT 'bibliographic reference in NLM''s MEDLINE format',
        PMID VARCHAR(1000) COMMENT 'PubMed Unique Identifier (PMID) for the citation in MEDLINE',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, reference_ctr)
) COMMENT 'Citations to publications related to the protocol results';

CREATE TABLE ct_responsible_party (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        party_ctr INT NOT NULL COMMENT 'Sequence of responsible party in list (internal primary key)',
        name_title VARCHAR(1000) COMMENT 'Old data format name and title',
        organization VARCHAR(1000) COMMENT 'Old data format organization',
	responsible_party_type VARCHAR(1000) COMMENT 'Sponsor, Investigator or Sponsor-Investigator',
	investigator_affiliation VARCHAR(1000) COMMENT 'primary organizational affiliation of the investigator',
	investigator_full_name VARCHAR(1000) COMMENT 'Full name of responsible investigator',
	investigator_title VARCHAR(1000) COMMENT 'title of the investigator, at the primary organizational affiliation',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, party_ctr)
) COMMENT 'As defined in US Public Law 110-85, Title VIII, Section 801,';

CREATE TABLE ct_keywords (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        keyword_ctr INT NOT NULL COMMENT 'Sequence of keyword in list (internal primary key)',
        keyword VARCHAR(1000) COMMENT 'Sequence of keyword in list (internal primary key)',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, keyword_ctr)
) COMMENT 'Keywords';

CREATE TABLE ct_browse_condition (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        condition_ctr INT NOT NULL COMMENT 'Sequence of condition in list (internal primary key)',
        mesh_term VARCHAR(1000) COMMENT 'Condition related MeSH term.', 
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, condition_ctr)
) COMMENT 'List of condition-related MeSH terms for browsing (Undocumented)';

CREATE TABLE ct_browse_intervention (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        intervention_ctr INT NOT NULL COMMENT 'Sequence of intervention in list (internal primary key)',
        mesh_term VARCHAR(1000) COMMENT 'Intervention related MeSH term.',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, intervention_ctr)
) COMMENT 'List of intervention-related MeSH terms for browsing (Undocumented)';

CREATE TABLE ct_results (
	id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
	results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
	recruitment_details VARCHAR(1000) COMMENT 'Key information relevant to the recruitment process for the overall study, such as dates of the recruitment period and types of location (e.g., medical clinic), to provide context.',
	pre_assignment_details VARCHAR(1000) COMMENT 'Description of any significant events and approaches for the overall study (e.g., wash out, run-in, transition) following participant enrollment, but prior to group assignment.',
	events_timeframe VARCHAR(1000) COMMENT 'Period in which the reported adverse event data were collected',
	events_desc VARCHAR(1000) COMMENT 'Additional relevant information about adverse event collection, including details about the method of systematic assessment',
	pi_employee VARCHAR(1000) COMMENT 'If all principal investigators are employees of the sponsor',
	restrictive_agreement VARCHAR(1000) COMMENT 'If there is an agreement between the sponsor (or its agent) and any non-employee PI(s) that restricts the PI''s rights to discuss or publish trial results after the trial is completed',
	limitations VARCHAR(1000) COMMENT 'describe significant limitations of the trial',
	poc_name_or_title VARCHAR(1000) COMMENT 'Point of contact for scientific information about the posted clinical trial results.',
	poc_organization VARCHAR(1000) COMMENT 'Full name of the designated individual''s organizational affiliation.',
	poc_phone VARCHAR(1000) COMMENT 'Office phone of the designated individual.',
	poc_email VARCHAR(1000) COMMENT 'Electronic mail address of the designated individual',
        FOREIGN KEY (id) REFERENCES ct_master(id) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr)
) COMMENT 'Reported Study Results';

CREATE TABLE ct_results_groups (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
	group_ctr INT NOT NULL COMMENT 'Sequence of group in list (internal primary key)',
        group_title VARCHAR(1000) COMMENT 'Label used to identify the arm or comparison group.',
        group_desc VARCHAR(1000) COMMENT 'Brief description of the arm or comparison group to distinguish it from other arms/groups in the trial.',
        group_id VARCHAR(1000) COMMENT 'Group Identifier (should match up to ct_arm_groups)',
        FOREIGN KEY (id, results_ctr) REFERENCES ct_results(id, results_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, group_ctr)
) COMMENT 'Arms or comparison groups in a trial';

CREATE TABLE ct_results_periods (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        period_ctr INT NOT NULL COMMENT 'Sequence of period in list (internal primary key)',
        period_title VARCHAR(1000) COMMENT 'Title describing a stage of the trial',
        FOREIGN KEY (id, results_ctr) REFERENCES ct_results(id, results_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, period_ctr)
) COMMENT 'Discrete stages of a clinical trial during which numbers of participants at specific significant events or points of time are reported.';

CREATE TABLE ct_results_periods_milestones (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        period_ctr INT NOT NULL COMMENT 'Sequence of period in list (internal primary key)',
	milestone_ctr INT NOT NULL COMMENT 'Sequence of milestone in list (internal primary key)',
        milestone_title VARCHAR(1000) COMMENT 'Label describing milestone',
        FOREIGN KEY (id, results_ctr, period_ctr) REFERENCES ct_results_periods(id, results_ctr, period_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, period_ctr, milestone_ctr)
) COMMENT 'Any specific events or time points in the trial when the numbers of participants are reported may be added.';

CREATE TABLE ct_results_periods_participants (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        period_ctr INT NOT NULL COMMENT 'Sequence of period in list (internal primary key)',
        milestone_ctr INT NOT NULL COMMENT 'Sequence of milestone in list (internal primary key)',
	participant_ctr INT NOT NULL COMMENT 'Sequence of participant group in list (internal primary key)',
        group_id VARCHAR(1000) COMMENT 'Group Identifier (should match up to ct_arm_groups)',
        group_desc VARCHAR(1000) COMMENT 'undocumented',
	count VARCHAR(1000) COMMENT 'Number of participants to reach the milestone.',
        FOREIGN KEY (id, results_ctr, period_ctr, milestone_ctr) REFERENCES ct_results_periods_milestones(id, results_ctr, period_ctr, milestone_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, period_ctr, milestone_ctr, participant_ctr)
) COMMENT 'Participant group at a given milestone';

CREATE TABLE ct_results_periods_drops (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        period_ctr INT NOT NULL COMMENT 'Sequence of period in list (internal primary key)',
        drops_ctr INT NOT NULL COMMENT 'Sequence of drop reason in list (internal primary key)',
        drop_reason_title VARCHAR(1000) COMMENT 'Specific reason not completed',
        FOREIGN KEY (id, results_ctr, period_ctr) REFERENCES ct_results_periods(id, results_ctr, period_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, period_ctr, drops_ctr)
) COMMENT 'Additional information about participants who did not complete the period.';

CREATE TABLE ct_results_periods_drops_participants (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        period_ctr INT NOT NULL COMMENT 'Sequence of period in list (internal primary key)',
        drops_ctr INT NOT NULL COMMENT 'Sequence of drop reason in list (internal primary key)',
        participant_ctr INT NOT NULL COMMENT 'Sequence of participant group in list (internal primary key)',
        group_id VARCHAR(1000) COMMENT 'Group Identifier (should match up to ct_arm_groups)',
	group_desc VARCHAR(1000) COMMENT 'undocumented',
        count VARCHAR(1000) COMMENT 'Number of participants to drop for the given reason.',
        FOREIGN KEY (id, results_ctr, period_ctr, drops_ctr) REFERENCES ct_results_periods_drops(id, results_ctr, period_ctr, drops_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, period_ctr, drops_ctr, participant_ctr)
) COMMENT 'Participant group for a given drop reason';

CREATE TABLE ct_results_baseline_groups (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        group_ctr INT NOT NULL COMMENT 'Sequence of group in list (internal primary key)',
	group_title VARCHAR(1000) COMMENT 'Label used to identify the arm or comparison group.', 
	group_desc VARCHAR(1000) COMMENT 'Brief description of the arm or comparison group to distinguish it from other arms/groups in the trial.',
	group_id VARCHAR(1000) COMMENT 'Group Identifier (should match up to ct_arm_groups)',
        FOREIGN KEY (id, results_ctr) REFERENCES ct_results(id, results_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, group_ctr)
) COMMENT 'Arms or comparison groups in the baseline of a trial';

CREATE TABLE ct_results_baseline_measures (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        measure_ctr INT NOT NULL COMMENT 'Sequence of measure in list (internal primary key)',
        measure_title VARCHAR(1000) COMMENT 'Measure title',
        measure_desc VARCHAR(1000) COMMENT 'Additional information about the measure, such as details about the collection method or participant population, if different from Overall Number of Baseline Participants.',
        units VARCHAR(1000) COMMENT 'Units of measure',
	param VARCHAR(1000) COMMENT 'Parameter measured',
	dispersion VARCHAR(1000) COMMENT 'Measure of dispersion',
        FOREIGN KEY (id, results_ctr) REFERENCES ct_results(id, results_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, measure_ctr)
) COMMENT 'Name and description of a characteristic measured at the beginning of the trial.';

CREATE TABLE ct_results_baseline_measure_categories (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        measure_ctr INT NOT NULL COMMENT 'Sequence of measure in list (internal primary key)',
        category_ctr INT NOT NULL COMMENT 'Sequence of category in list (internal primary key)',
        sub_title VARCHAR(1000) COMMENT 'Name of distinct category used to measure outcome, if reporting categorical data.',
        FOREIGN KEY (id, results_ctr, measure_ctr) REFERENCES ct_results_baseline_measures(id, results_ctr, measure_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, measure_ctr, category_ctr)
) COMMENT 'Name and description of a category of a characteristic measured at the beginning of the trial.';

CREATE TABLE ct_results_baseline_measure_values (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        measure_ctr INT NOT NULL COMMENT 'Sequence of measure in list (internal primary key)',
	category_ctr INT NOT NULL COMMENT 'Sequence of value in list (internal primary key)',
	value_ctr INT NOT NULL COMMENT 'Sequence of category in list (internal primary key)',
	group_id VARCHAR(1000) COMMENT 'Group Identifier (should match up to ct_arm_groups)',
	value VARCHAR(1000) COMMENT 'Measurement Value',
	spread VARCHAR(1000) COMMENT 'Spread of Results',
	lower_limit VARCHAR(1000) COMMENT 'Lower Limit of Results',
	upper_limit VARCHAR(1000) COMMENT 'Upper Limit of Results',
	value_note VARCHAR(1000) COMMENT 'annotation',
        FOREIGN KEY (id, results_ctr, measure_ctr, category_ctr) REFERENCES ct_results_baseline_measure_categories(id, results_ctr, measure_ctr, category_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, measure_ctr, category_ctr, value_ctr)
) COMMENT 'Values measured as part of the baseline of a trial.';

CREATE TABLE ct_results_outcomes (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        outcome_ctr INT NOT NULL COMMENT 'Sequence of outcome in list (internal primary key)',
	outcome_type VARCHAR(1000) COMMENT 'Primary, Secondary, Other pre-speciified or Post-Hoc',
	outcome_title VARCHAR(1000) COMMENT 'Name of outcome measure',
	outcome_desc VARCHAR(1000) COMMENT 'Additional information about outcome measure.',
	time_frame VARCHAR(1000) COMMENT 'Time point(s) at which outcome measure was assessed.',
	safety_issue VARCHAR(1000) COMMENT 'Is this outcome measure assessing a safety issue?',
	posting_date VARCHAR(1000) COMMENT 'If results data are not included for an outcome measure, provide the expected month and year they will be submitted.',
	population VARCHAR(1000) COMMENT 'Explanation of how the number of participants for analysis was determined.',
        FOREIGN KEY (id, results_ctr) REFERENCES ct_results(id, results_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, outcome_ctr)
) COMMENT 'Name and description of the measure used to assess the effect of experimental variables in the trial';

CREATE TABLE ct_results_outcomes_groups (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        outcome_ctr INT NOT NULL COMMENT 'Sequence of outcome in list (internal primary key)',
        group_ctr INT NOT NULL COMMENT 'Sequence of group in list (internal primary key)',
        group_title VARCHAR(1000) COMMENT 'Label used to identify the arm or comparison group.',
        group_desc VARCHAR(1000) COMMENT 'Brief description of the arm or comparison group to distinguish it from other arms/groups in the trial.',
        group_id VARCHAR(1000) COMMENT 'Group Identifier (should match up to ct_arm_groups)',
        FOREIGN KEY (id, results_ctr, outcome_ctr) REFERENCES ct_results_outcomes(id, results_ctr, outcome_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, outcome_ctr, group_ctr)
) COMMENT 'Arms or comparison groups in a trial';

CREATE TABLE ct_results_outcomes_measures (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        outcome_ctr INT NOT NULL COMMENT 'Sequence of outcome in list (internal primary key)',
        measure_ctr INT NOT NULL COMMENT 'Sequence of measure in list (internal primary key)',
        measure_title VARCHAR(1000) COMMENT 'Measure title',
        measure_desc VARCHAR(1000) COMMENT 'Additional information about the measure, such as details about the collection method or participant population, if different from Overall Number of Baseline Participants.',
        units VARCHAR(1000) COMMENT 'Units of measure',
        param VARCHAR(1000) COMMENT 'Parameter measured',
        dispersion VARCHAR(1000) COMMENT 'Measure of dispersion',
        FOREIGN KEY (id, results_ctr, outcome_ctr) REFERENCES ct_results_outcomes(id, results_ctr, outcome_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, outcome_ctr, measure_ctr)
) COMMENT 'Name and description of a characteristic measured.';

CREATE TABLE ct_results_outcomes_measure_categories (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
	outcome_ctr INT NOT NULL COMMENT 'Sequence of outcome in list (internal primary key)',
        measure_ctr INT NOT NULL COMMENT 'Sequence of measure in list (internal primary key)',
        category_ctr INT NOT NULL COMMENT 'Sequence of category in list (internal primary key)',
        sub_title VARCHAR(1000) COMMENT 'Name of distinct category used to measure outcome, if reporting categorical data.',
        FOREIGN KEY (id, results_ctr, outcome_ctr, measure_ctr) REFERENCES ct_results_outcomes_measures(id, results_ctr, outcome_ctr, measure_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, outcome_ctr, measure_ctr, category_ctr)
) COMMENT 'Name and description of category of a characteristic measured.';

CREATE TABLE ct_results_outcomes_measure_values (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
	outcome_ctr INT NOT NULL COMMENT 'Sequence of outcome in list (internal primary key)',
        measure_ctr INT NOT NULL COMMENT 'Sequence of measure in list (internal primary key)',
        category_ctr INT NOT NULL COMMENT 'Sequence of value in list (internal primary key)',
        value_ctr INT NOT NULL COMMENT 'Sequence of category in list (internal primary key)',
        group_id VARCHAR(1000) COMMENT 'Group Identifier (should match up to ct_arm_groups)',
        value VARCHAR(1000) COMMENT 'Measurement Value',
        spread VARCHAR(1000) COMMENT 'Spread of Results',
        lower_limit VARCHAR(1000) COMMENT 'Lower Limit of Results',
        upper_limit VARCHAR(1000) COMMENT 'Upper Limit of Results',
        value_note VARCHAR(1000) COMMENT 'annotation',
        FOREIGN KEY (id, results_ctr, outcome_ctr, measure_ctr, category_ctr) REFERENCES ct_results_outcomes_measure_categories(id, results_ctr, outcome_ctr, measure_ctr, category_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, outcome_ctr, measure_ctr, category_ctr, value_ctr)
) COMMENT 'Values measured as part of an outcome.';

CREATE TABLE ct_results_analysis (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        outcome_ctr INT NOT NULL COMMENT 'Sequence of outcome in list (internal primary key)',
        analysis_ctr INT NOT NULL COMMENT 'Sequence of analysis in list (internal primary key)',
        groups_desc VARCHAR(1000) COMMENT 'Additional details about the statistical analysis, such as null hypothesis and description of power calculation',
        non_inferiority VARCHAR(1000) COMMENT 'Identifies whether the analysis is a test of non-inferiority or equivalence',
        non_inferiority_desc VARCHAR(1000) COMMENT 'If, "Yes", provide additional details, including details of the power calculation (if not previously provided), definition of non-inferiority margin, and other key parameters',
        p_value VARCHAR(1000) COMMENT 'Calculated p-value given the null-hypothesis',
	p_value_desc VARCHAR(1000) COMMENT 'Additional information, such as whether or not the p-value is adjusted for multiple comparisons and the a priori threshold for statistical significance',
	method VARCHAR(1000) COMMENT 'Procedure used to estimate effect of intervention.',
        method_desc VARCHAR(1000) COMMENT 'Undocumented',
        param_type VARCHAR(1000) COMMENT 'Estimation Parameter Type',
        param_value VARCHAR(1000) COMMENT 'Estimateion Parameter Value',
        dispersion_type VARCHAR(1000) COMMENT 'Standard deviation or Standard Error of the Mean',
        dispersion_value VARCHAR(1000) COMMENT 'Value of dispersionmeasure',
        ci_percent VARCHAR(1000) COMMENT 'Level of confidence interval, expressed as a percent',
        ci_n_sides VARCHAR(1000) COMMENT 'Number of sides of confidence interval',
        ci_lower_limit VARCHAR(1000) COMMENT 'Lower limit of confidence interval',
        ci_upper_limit VARCHAR(1000) COMMENT 'Upper limit of confidence interval',
        ci_upper_limit_na_comment VARCHAR(1000) COMMENT 'Explain why the upper limit data are Not Available.',
        estimate_desc VARCHAR(1000) COMMENT 'Any other relevant estimation information, including the direction of the comparison (e.g., describe which arm or comparison group represents the numerator and denominator for relative risk)',
        FOREIGN KEY (id, results_ctr, outcome_ctr) REFERENCES ct_results_outcomes(id, results_ctr, outcome_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, outcome_ctr, analysis_ctr)
) COMMENT 'Summary description of the analysis performed.';

CREATE TABLE ct_results_analysis_groups (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        outcome_ctr INT NOT NULL COMMENT 'Sequence of outcome in list (internal primary key)',
        analysis_ctr INT NOT NULL COMMENT 'Sequence of analysis in list (internal primary key)',
	group_ctr INT NOT NULL COMMENT 'Sequence of group in list (internal primary key)',
	group_id VARCHAR(1000) COMMENT 'Group Identifier (should match up to ct_arm_groups)',
        FOREIGN KEY (id, results_ctr, outcome_ctr, analysis_ctr) REFERENCES ct_results_analysis(id, results_ctr, outcome_ctr, analysis_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, outcome_ctr, analysis_ctr, group_ctr)
) COMMENT 'Identifies the arms or comparison groups involved in the statistical analysis';

CREATE TABLE ct_results_events_groups (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        group_ctr INT NOT NULL COMMENT 'Sequence of group in list (internal primary key)',
	group_title VARCHAR(1000) COMMENT 'Label used to identify the arm or comparison group.',
	group_desc VARCHAR(1000) COMMENT 'Brief description of the arm or comparison group to distinguish it from other arms/groups in the trial.',
        group_id VARCHAR(1000) COMMENT 'Group Identifier (should match up to ct_arm_groups)',
        FOREIGN KEY (id, results_ctr) REFERENCES ct_results(id, results_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, group_ctr)	
) COMMENT 'Arms or comparison groups in a trial';

CREATE TABLE ct_results_events_serious (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
	serious_events_ctr INT NOT NULL COMMENT 'Sequence of serious event in list (internal primary key)',
	frequency_threshhold VARCHAR(1000) COMMENT 'The frequency of Other (Not Including Serious) Adverse Events that, when exceeded within any arm or comparison group, are reported in the results database for all arms or comparison groups.',
	default_vocab VARCHAR(1000) COMMENT 'Default terminology used to describe events',
	default_assessment VARCHAR(1000) COMMENT 'Default method of assessing events',
        FOREIGN KEY (id, results_ctr) REFERENCES ct_results(id, results_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, serious_events_ctr)
) COMMENT 'adverse events that result in death, require either inpatient hospitalization or the prolongation of hospitalization, are life-threatening, result in a persistent or significant disability/incapacity or result in a congenita
l anomaly/birth defect.';

CREATE TABLE ct_results_events_serious_categories (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        serious_events_ctr INT NOT NULL COMMENT 'Sequence of serious event in list (internal primary key)',
	category_ctr INT NOT NULL COMMENT 'Sequence of category in list (internal primary key)',
        category_title VARCHAR(1000) COMMENT 'title of the category.',
        FOREIGN KEY (id, results_ctr, serious_events_ctr) REFERENCES ct_results_events_serious(id, results_ctr, serious_events_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, serious_events_ctr, category_ctr)
) COMMENT 'Categories of serious adverse events';

CREATE TABLE ct_results_events_serious_events (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        serious_events_ctr INT NOT NULL COMMENT 'Sequence of serious event in list (internal primary key)',
        category_ctr INT NOT NULL COMMENT 'Sequence of category in list (internal primary key)',
	event_ctr INT NOT NULL COMMENT 'Sequence of event in list (internal primary key)',
        sub_title VARCHAR(1000) COMMENT 'title of the events.',
	assessment VARCHAR(1000) COMMENT 'Method used to assess the adverse event.',
	event_desc VARCHAR(1000) COMMENT 'Additional relevant information about the adverse event, including any deviation from the Time Frame for Adverse Event Reporting.',
        FOREIGN KEY (id, results_ctr, serious_events_ctr, category_ctr) REFERENCES ct_results_events_serious_categories(id, results_ctr, serious_events_ctr, category_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, serious_events_ctr, category_ctr, event_ctr)
) COMMENT 'Specific types of serious adverse events';

CREATE TABLE ct_results_events_serious_counts (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        serious_events_ctr INT NOT NULL COMMENT 'Sequence of serious event in list (internal primary key)',
        category_ctr INT NOT NULL COMMENT 'Sequence of category in list (internal primary key)',
        event_ctr INT NOT NULL COMMENT 'Sequence of event in list (internal primary key)',
	count_ctr INT NOT NULL COMMENT 'Sequence of count in list (internal primary key)',
        group_id VARCHAR(1000) COMMENT 'Group Identifier (should match up to ct_arm_groups)',
        subjects_affected VARCHAR(1000) COMMENT 'Number of participants experiencing at least one event being reported ',
        subjects_at_risk VARCHAR(1000) COMMENT 'Number of participants assessed for adverse events during the trial (i.e., the denominator for calculating frequency of adverse events).',
	event_count VARCHAR(1000) COMMENT 'Number of occurrences of the adverse event being reported',
        FOREIGN KEY (id, results_ctr, serious_events_ctr, category_ctr, event_ctr) REFERENCES ct_results_events_serious_events(id, results_ctr, serious_events_ctr, category_ctr, event_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, serious_events_ctr, category_ctr, event_ctr, count_ctr)
) COMMENT 'Counts of serious adverse events by event and by group';

CREATE TABLE ct_results_events_other (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        other_events_ctr INT NOT NULL COMMENT 'Sequence of other event in list (internal primary key)',
        frequency_threshhold VARCHAR(1000) COMMENT 'The frequency of Other (Not Including Serious) Adverse Events that, when exceeded within any arm or comparison group, are reported in the results database for all arms or comparison groups.',
        default_vocab VARCHAR(1000) COMMENT 'Default terminology used to describe events',
        default_assessment VARCHAR(1000) COMMENT 'Default method of assessing events',
        FOREIGN KEY (id, results_ctr) REFERENCES ct_results(id, results_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, other_events_ctr)
) COMMENT 'Other (Not Including Serious) Adverse Events are those that are not Serious Adverse Events that exceed a frequency threshold.';

CREATE TABLE ct_results_events_other_categories (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        other_events_ctr INT NOT NULL COMMENT 'Sequence of other event in list (internal primary key)',
        category_ctr INT NOT NULL COMMENT 'Sequence of category in list (internal primary key)',
        category_title VARCHAR(1000) COMMENT 'title of the category.',
        FOREIGN KEY (id, results_ctr, other_events_ctr) REFERENCES ct_results_events_other(id, results_ctr, other_events_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, other_events_ctr, category_ctr)
) COMMENT 'Categories of other adverse events';

CREATE TABLE ct_results_events_other_events (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        other_events_ctr INT NOT NULL COMMENT 'Sequence of other event in list (internal primary key)',
        category_ctr INT NOT NULL COMMENT 'Sequence of category in list (internal primary key)',
        event_ctr INT NOT NULL COMMENT 'Sequence of event in list (internal primary key)',
        sub_title VARCHAR(1000) COMMENT 'title of the events.',
        assessment VARCHAR(1000) COMMENT 'Method used to assess the adverse event.',
        event_desc VARCHAR(1000) COMMENT 'Additional relevant information about the adverse event, including any deviation from the Time Frame for Adverse Event Reporting.',
        FOREIGN KEY (id, results_ctr, other_events_ctr, category_ctr) REFERENCES ct_results_events_other_categories(id, results_ctr, other_events_ctr, category_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, other_events_ctr, category_ctr, event_ctr)
) COMMENT 'Specific types of other adverse events';

CREATE TABLE ct_results_events_other_counts (
        id VARCHAR(15) NOT NULL COMMENT 'Record ID (internal primary key)',
        results_ctr INT NOT NULL COMMENT 'Sequence of results in list (internal primary key)',
        other_events_ctr INT NOT NULL COMMENT 'Sequence of other event in list (internal primary key)',
        category_ctr INT NOT NULL COMMENT 'Sequence of category in list (internal primary key)',
        event_ctr INT NOT NULL COMMENT 'Sequence of event in list (internal primary key)',
        count_ctr INT NOT NULL COMMENT 'Sequence of count in list (internal primary key)',
        group_id VARCHAR(1000) COMMENT 'Group Identifier (should match up to ct_arm_groups)',
        subjects_affected VARCHAR(1000) COMMENT 'Number of participants experiencing at least one event being reported ',
        subjects_at_risk VARCHAR(1000) COMMENT 'Number of participants assessed for adverse events during the trial (i.e., the denominator for calculating frequency of adverse events).',
        event_count VARCHAR(1000) COMMENT 'Number of occurrences of the adverse event being reported',
        FOREIGN KEY (id, results_ctr, other_events_ctr, category_ctr, event_ctr) REFERENCES ct_results_events_other_events(id, results_ctr, other_events_ctr, category_ctr, event_ctr) ON DELETE CASCADE,
        UNIQUE KEY (id, results_ctr, other_events_ctr, category_ctr, event_ctr, count_ctr)
) COMMENT 'Counts of other adverse events by event and by group';

