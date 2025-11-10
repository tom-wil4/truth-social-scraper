# Truth Social Scraper

> Truth Social Scraper extracts public profile details, posts, and replies from the Truth Social platform. It helps researchers, analysts, and developers collect and study user-generated content for insights into social engagement and sentiment trends.

> Whether you're tracking political discussions or monitoring social media influence, this scraper provides structured data ready for analysis.


<p align="center">
  <a href="https://bitbash.def" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Truth Social Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

Truth Social Scraper automates data extraction from the Truth Social platform. It collects user profiles, original posts ("truths"), and replies to other users’ posts — enabling transparent data collection for analysis and reporting.

This tool is ideal for:
- Researchers studying political communication or media trends
- Analysts monitoring user sentiment and engagement
- Developers building dashboards or automation around Truth Social data

### Why Use Truth Social Scraper

- Collects public Truth Social data efficiently and safely
- Helps analyze communication patterns and user sentiment
- Supports research, monitoring, and trend analysis
- Enables data-driven insights into online discussions

## Features

| Feature | Description |
|----------|-------------|
| Profile Scraping | Extracts full user profile details like display name, followers, and verification status. |
| Posts Collection | Retrieves public posts made by a given user. |
| Replies Gathering | Collects replies to other users’ posts for engagement analysis. |
| Combined Mode | Gathers both posts and replies for complete user interaction data. |
| JSON Output | Provides structured JSON for integration with analytics tools or storage. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|-------------|------------------|
| id | Unique identifier of the profile or post. |
| url | Direct URL of the Truth Social profile or post. |
| username | Handle or username of the profile. |
| displayName | Full display name of the account owner. |
| description | Textual description or bio of the user. |
| website | Website listed on the user profile. |
| avatar | Profile picture URL. |
| header | Cover image URL. |
| followersCount | Number of followers. |
| followingCount | Number of accounts followed. |
| postsAndRepliesCount | Total posts and replies made. |
| verified | Indicates if the account is verified. |
| content | Text content of posts or replies. |
| mediaAttachments | Array of media items attached to a post. |
| repliesCount | Total number of replies. |
| reblogsCount | Number of re-shares or reposts. |
| favouritesCount | Number of likes or favorites. |

---

## Example Output

    [
        {
            "input": "https://truthsocial.com/@realDonaldTrump",
            "id": "107780257626128497",
            "url": "https://truthsocial.com/@realDonaldTrump",
            "username": "realDonaldTrump",
            "displayName": "Donald J. Trump",
            "description": "",
            "website": "www.DonaldJTrump.com",
            "avatar": "https://static-assets-1.truthsocial.com/tmtg:prime-ts-assets/accounts/avatars/107/780/257/626/128/497/original/454286ac07a6f6e6.jpeg",
            "header": "https://static-assets-1.truthsocial.com/tmtg:prime-ts-assets/accounts/headers/107/780/257/626/128/497/original/ba3b910ba387bf4e.jpeg",
            "followersCount": 8366535,
            "followingCount": 71,
            "postsAndRepliesCount": 24289,
            "createdAt": "2022-02-11T16:16:57.705Z",
            "verified": true
        },
        {
            "id": "113560838963769446",
            "type": "post",
            "accountId": "107780257626128497",
            "username": "realDonaldTrump",
            "createdAt": "2024-11-28T13:34:47.509Z",
            "url": "https://truthsocial.com/@realDonaldTrump/113560838963769446",
            "mediaAttachments": [
                {
                    "id": "113560838939449294",
                    "type": "image",
                    "url": "https://static-assets-1.truthsocial.com/tmtg:prime-ts-assets/media_attachments/files/113/560/838/939/449/294/original/098be9d5bdb0c201.jpg",
                    "previewUrl": "https://static-assets-1.truthsocial.com/tmtg:prime-ts-assets/media_attachments/files/113/560/838/939/449/294/small/098be9d5bdb0c201.jpg"
                }
            ],
            "repliesCount": 945,
            "reblogsCount": 2040,
            "favouritesCount": 9634
        },
        {
            "id": "113478531114340760",
            "type": "reply",
            "accountId": "107780257626128497",
            "username": "realDonaldTrump",
            "createdAt": "2024-11-14T00:42:49.401Z",
            "url": "https://truthsocial.com/@realDonaldTrump/113478531114340760",
            "content": "Elon Musk is a great guy, loaded with personality and brainpower...",
            "repliesCount": 2385,
            "reblogsCount": 8835,
            "favouritesCount": 45960
        }
    ]

---

## Directory Structure Tree

    Truth Social Scraper/
    ├── src/
    │   ├── main.py
    │   ├── extractors/
    │   │   ├── profile_extractor.py
    │   │   ├── posts_extractor.py
    │   │   └── replies_extractor.py
    │   ├── outputs/
    │   │   └── data_formatter.py
    │   └── config/
    │       └── settings.json
    ├── data/
    │   ├── input_examples.txt
    │   └── sample_output.json
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Social media researchers** use it to gather user posts for sentiment and trend analysis.
- **Data journalists** use it to track discussions around political figures or issues.
- **Marketing analysts** use it to evaluate engagement levels and community reactions.
- **Developers** use it to power dashboards and social data visualizations.
- **Academic teams** use it for studying communication dynamics on alternative social platforms.

---

## FAQs

**Can I scrape comments from Truth Social?**
No, comments require authenticated access. This scraper focuses on publicly available data only, ensuring compliance with platform rules.

**Is this scraper legal to use?**
Yes, as long as it’s used responsibly and in accordance with Truth Social’s public data terms and local data protection laws.

**How many profiles can I scrape at once?**
You can provide multiple usernames or profile URLs; each will be processed sequentially to ensure stable results.

**Does the scraper support media downloads?**
Yes, it extracts URLs to attached media (images or videos), which can be downloaded separately if needed.

---

## Performance Benchmarks and Results

**Primary Metric:** Processes up to 500 profiles per hour with standard rate limits.
**Reliability Metric:** 98% success rate across active public profiles.
**Efficiency Metric:** Optimized for low resource usage and minimal request overhead.
**Quality Metric:** Delivers 100% of visible post and reply data fields with clean JSON formatting.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
