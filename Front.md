# Frontend

## About
In order to expand our project, at first we talked about developing a frontend-like app so we could ***actually use*** the results of the requested Recommendation Model. This was because the only way we had to show the results was through an Excel or CSV file. I personally (Franco) felt that it would be better show the results as a final User would get them.

## Process

At first, I started working with Streamlit, a library mostly used for reports and Analytics. However, I decided to explore for other possibilities like Flask and Django since I wasn't confortable enough with Streamlit. During learning process I realized that Flask was the best option, so I went for it.

## Development

My first task was to create all the models related to the BigQuery tables, therefore I ended up creating the models that correspond to **metadata** and the table with all the reviews, plus 7 more tables:

- Products (metadata):
    1. Asin (Unique identifier)
    1. Title (Name of the product)
    1. Description (Description of the product)
    1. Brand
    1. Price
    1. ImUrl (Image of the product)
    1. Categories (List of the categories that the product belongs to)
    1. Bought together (List of the products that were bought in the same cart, by *asin*)
    1. Buy after viewing (By *asin*)
    1. Also bought
    1. Also viewed
    1. Sales rank
    1. User id (User's unique identifier)
    
- Reviews:
    1. Id (Unique identifier)
    1. Asin (The product that was posted in)
    1. Reviewer ID (User's unique identifier)
    1. Reviewer name (Username of the reviewer)
    1. Summary (Title of the review)
    1. Review text (Content of the review)
    1. Overall (Rating of the product)
    1. Date (When the review was posted)
    1. Unix review time (Same as **date** but in unix format)
    1. Category (Category of the product)
    1. CategoryN (Numeric representation of the category)
    1. Helpful (Positive or negative votes for the review)
    
- Users:
    1. Id (Unique identifier)
    1. Creation date
    1. Username
    1. Email
    1. Pfp (Profile picture)
    1. Password (A password that has been hashed)
    
- Users Cart/Discounts/Favorites/Purchases (Since all these tables have the same columns):
    1. Id (Unique identifier)
    1. User id (User's unique identifier)
    1. Asin (Product's unique identifier)
    
- Users Helpful/Not Helpful (User's votes):
    1. Id (Unique identifier)
    1. User id (User's unique identifier)
    1. Review (Review's unique identifier)
    
After all models were created, I spent ~1 week designing the frontend and all it's routes. For the visual interface I used Bootstrap, since it made everything so much easier.

## Conclusion:

I ended up with 7 folders, 1 subfolder and 46 files (Including 23 HTML templates).

This was my first time working with so much files and this amount of data. I really enjoyed the learning process since I used a lot of the acquired knowledge during classes and the previous Individual Projects (PIs 01, 02 and 03)

## Snapshots:

![Home](https://i.imgur.com/p4K4cd7.png)

![Loading page](https://i.imgur.com/jO1UWQm.png)

![Register](https://i.imgur.com/j90Fs1R.png)

![Login](https://i.imgur.com/BgZGMCu.png)

![Discounts](https://i.imgur.com/wOwBmvY.png)

![Catalog](https://i.imgur.com/WdYFYrE.png)

![Category](https://i.imgur.com/zh0hpFb.png)

![Product](https://i.imgur.com/uy0UUWp.png)

![Checkout](https://i.imgur.com/4erNaM5.png)

![Post checkout](https://i.imgur.com/4ZrmB6w.png)

![About](https://i.imgur.com/uedA15N.png)

![Profile](https://i.imgur.com/jrXCoRR.png)

![Favorites](https://i.imgur.com/v08dZf5.png)

![Cart](https://i.imgur.com/KyXSOfW.png)

![Reviews](https://i.imgur.com/U0SAgMh.png)

![Update profile](https://i.imgur.com/ABh24rJ.png)

![Change password](https://i.imgur.com/nTBGbnB.png)
