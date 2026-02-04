# E-Commerce Analysis Dashboard

## 📊 Project Overview
Proyek analisis data komprehensif terhadap Brazilian E-Commerce Public Dataset dari Olist. Analisis ini mencakup tiga aspek utama:
1. **Customer Satisfaction & Delivery Performance** - Analisis hubungan antara ketepatan pengiriman dengan kepuasan pelanggan
2. **RFM Customer Segmentation** - Segmentasi pelanggan berdasarkan Recency, Frequency, dan Monetary value
3. **Geospatial Revenue Distribution** - Analisis distribusi geografis revenue dan peluang ekspansi

## 📁 Project Structure
```
submission/
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
├── data/
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## 🔧 Setup Environment

### Prerequisites
- Python 3.9 atau lebih tinggi
- pip (Python package manager)

### Installation

1. **Clone atau Download Project**
```bash
   cd submission
```

2. **Install Dependencies**
```bash
   pip install -r requirements.txt
```
   
   Atau install manual:
```bash
   pip install pandas==2.3.2 numpy==1.23.5 matplotlib==3.9.4 seaborn==0.13.2 streamlit==1.41.1
```

## 🚀 Running the Dashboard

### Menjalankan Dashboard Secara Lokal

1. **Navigate ke direktori dashboard**
```bash
   cd dashboard
```

2. **Run Streamlit app**
```bash
   streamlit run dashboard.py
```

3. **Akses dashboard**
   - Dashboard akan otomatis terbuka di browser
   - Jika tidak, buka: `http://localhost:8501`

### Catatan Penting
- Pastikan file `main_data.csv` ada di direktori `dashboard/`
- File ini di-generate otomatis dari notebook analysis

## 📊 Dashboard Features

### 1. Overview Page
- Key business metrics (Total Orders, Customers, Revenue, Avg Review)
- Monthly orders trend
- Review score distribution
- Top 10 product categories

### 2. Delivery Performance Analysis
- Average delivery time metrics
- On-time delivery rate
- Impact of delivery delays on customer satisfaction
- Satisfaction rate by delay category
- Interactive insights and recommendations

### 3. RFM Customer Segmentation
- Customer segmentation based on Recency, Frequency, Monetary
- 8 distinct customer segments:
  - Champions
  - Loyal Customers
  - Potential Loyalist
  - Recent Customers
  - At Risk
  - Can't Lose Them
  - Hibernating
  - Need Attention
- Revenue contribution by segment
- Segment-specific recommendations

### 4. Geospatial Analysis
- Revenue distribution by Brazilian states
- Customer density mapping
- Market concentration analysis
- Growth opportunity identification
- State performance categorization

## 🎯 Key Findings

### Delivery Performance
- ✅ On-time deliveries: 4.21 avg review (79.6% satisfaction)
- ❌ Delayed deliveries: 2.55 avg review (48.9% satisfaction)
- ⚠️ Delays >7 days: 75%+ dissatisfaction rate

### RFM Segmentation
- 🏆 Champions: 6.92% customers, R$ 443 avg value
- ⚠️ At Risk: 23.81% customers (largest segment!)
- 💰 Total revenue concentration in top 3 segments

### Geographic Distribution
- 🗺️ SP dominates: 37.5% market share
- 📊 Top 5 states: 73.43% total revenue
- 🎯 Growth potential in High-Value states (PB, AC, AP)

## 📈 Business Recommendations

1. **Improve Delivery Performance**
   - Target: 95% on-time delivery rate
   - Implement predictive analytics for delay prevention
   - Proactive customer communication

2. **Customer Retention Strategy**
   - Win-back campaigns for "At Risk" segment (R$ 4.74M opportunity)
   - VIP programs for Champions
   - Onboarding for Potential Loyalists

3. **Geographic Expansion**
   - Maintain dominance in SP, RJ, MG
   - Expand to High-Value states (PR, BA, GO)
   - Develop North/Northeast presence

## 👨‍💻 Author
- **Nama**: [Your Name]
- **Email**: [Your Email]
- **ID Dicoding**: [Your Dicoding ID]

## 📝 Dataset Source
Brazilian E-Commerce Public Dataset by Olist
- Period: September 2016 - August 2018
- Total Orders: 96,478 delivered orders
- Source: Kaggle / Olist

## 📄 License
This project is for educational purposes as part of Dicoding's Data Analysis course.

## 🙏 Acknowledgments
- Dicoding Indonesia untuk platform pembelajaran
- Olist untuk menyediakan dataset
- Brazilian E-Commerce community

---
**Last Updated**: February 2026
