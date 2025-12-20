# mock_data.py

MOCK_DATA = {
            "hastaneler": [
                # Ankara - Çankaya
                {
                    "id": 1,
                    "adi": "Ankara Şehir Hastanesi",
                    "konum_il": "Ankara",
                    "konum_ilce": "Çankaya",
                    "koordinatlar": {"enlem": 39.9174, "boylam": 32.8532},
                    "poliklinikler": ["Kardiyoloji", "KBB", "Nöroloji", "Cildiye"]
                },
                {
                    "id": 2,
                    "adi": "Ankara Eğitim ve Araştırma Hastanesi",
                    "konum_il": "Ankara",
                    "konum_ilce": "Çankaya",
                    "koordinatlar": {"enlem": 39.9208, "boylam": 32.8541},
                    "poliklinikler": ["Kardiyoloji", "KBB", "Nöroloji", "Cildiye"]
                },

                # İstanbul - Fatih
                {
                    "id": 3,
                    "adi": "İstanbul Üniversitesi Çapa Tıp Fakültesi",
                    "konum_il": "İstanbul",
                    "konum_ilce": "Fatih",
                    "koordinatlar": {"enlem": 41.0189, "boylam": 28.9324},
                    "poliklinikler": ["Kardiyoloji", "KBB", "Nöroloji", "Cildiye"]
                },
                {
                    "id": 4,
                    "adi": "Haseki Eğitim ve Araştırma Hastanesi",
                    "konum_il": "İstanbul",
                    "konum_ilce": "Fatih",
                    "koordinatlar": {"enlem": 41.0182, "boylam": 28.9431},
                    "poliklinikler": ["Kardiyoloji", "KBB", "Nöroloji", "Cildiye"]
                },

                # İzmir - Bornova
                {
                    "id": 5,
                    "adi": "Ege Üniversitesi Hastanesi",
                    "konum_il": "İzmir",
                    "konum_ilce": "Bornova",
                    "koordinatlar": {"enlem": 38.4616, "boylam": 27.2023},
                    "poliklinikler": ["Kardiyoloji", "KBB", "Nöroloji", "Cildiye"]
                },
                {
                    "id": 6,
                    "adi": "Bornova Devlet Hastanesi",
                    "konum_il": "İzmir",
                    "konum_ilce": "Bornova",
                    "koordinatlar": {"enlem": 38.4671, "boylam": 27.2195},
                    "poliklinikler": ["Kardiyoloji", "KBB", "Nöroloji", "Cildiye"]
                },

                # Yozgat - Sorgun
                {
                    "id": 7,
                    "adi": "Sorgun Devlet Hastanesi",
                    "konum_il": "Yozgat",
                    "konum_ilce": "Sorgun",
                    "koordinatlar": {"enlem": 39.4616, "boylam": 33.2023},
                    "poliklinikler": ["Kardiyoloji", "KBB", "Nöroloji", "Cildiye"]
                },
                {
                    "id": 8,
                    "adi": "Yozgat Devlet Hastanesi ",
                    "konum_il": "Yozgat",
                    "konum_ilce": "Sorgun",
                    "koordinatlar": {"enlem": 39.4671, "boylam": 33.2195},
                    "poliklinikler": ["Kardiyoloji", "KBB", "Nöroloji", "Cildiye"]
                }
            ],
            "doktorlar": [
                # Ankara - Çankaya (hastane_id 1 ve 2)
                {"id": 101, "adi": "Dr. Ayşe Yılmaz", "uzmanlik": "Kardiyoloji", "hastane_id": 1,
                "musaitlik": {"2025-08-10": ["09:00", "10:30"], "2025-08-11": ["11:00"]}},
                {"id": 201, "adi": "Dr. Emre Şahin", "uzmanlik": "Kardiyoloji", "hastane_id": 1,
                "musaitlik": {"2025-08-12": ["09:00", "11:00"], "2025-08-13": ["14:00"]}},

                {"id": 102, "adi": "Dr. Mehmet Kaya", "uzmanlik": "Kardiyoloji", "hastane_id": 2,
                "musaitlik": {"2025-08-10": ["14:00"], "2025-08-12": ["09:00"]}},
                {"id": 202, "adi": "Dr. Selin Özkan", "uzmanlik": "Kardiyoloji", "hastane_id": 2,
                "musaitlik": {"2025-08-11": ["10:00"], "2025-08-14": ["13:00"]}},

                {"id": 103, "adi": "Dr. Zeynep Can", "uzmanlik": "KBB", "hastane_id": 1,
                "musaitlik": {"2025-08-10": ["11:00"], "2025-08-12": ["10:00"]}},
                {"id": 203, "adi": "Dr. Burak Yıldırım", "uzmanlik": "KBB", "hastane_id": 1,
                "musaitlik": {"2025-08-13": ["09:00", "15:00"]}},

                {"id": 104, "adi": "Dr. Cemal Demir", "uzmanlik": "KBB", "hastane_id": 2,
                "musaitlik": {"2025-08-11": ["09:30"], "2025-08-13": ["15:00"]}},
                {"id": 204, "adi": "Dr. İrem Akın", "uzmanlik": "KBB", "hastane_id": 2,
                "musaitlik": {"2025-08-14": ["10:00"], "2025-08-15": ["14:00"]}},

                {"id": 105, "adi": "Dr. Nihat Aksoy", "uzmanlik": "Nöroloji", "hastane_id": 1,
                "musaitlik": {"2025-08-10": ["16:00"], "2025-08-14": ["09:00"]}},
                {"id": 205, "adi": "Dr. Sibel Kara", "uzmanlik": "Nöroloji", "hastane_id": 1,
                "musaitlik": {"2025-08-15": ["10:00"], "2025-08-16": ["13:00"]}},

                {"id": 106, "adi": "Dr. Elif Güneş", "uzmanlik": "Nöroloji", "hastane_id": 2,
                "musaitlik": {"2025-08-12": ["13:00"], "2025-08-15": ["11:00"]}},
                {"id": 206, "adi": "Dr. Deniz Topal", "uzmanlik": "Nöroloji", "hastane_id": 2,
                "musaitlik": {"2025-08-16": ["09:00"], "2025-08-17": ["14:00"]}},

                {"id": 107, "adi": "Dr. Nihal Dinç", "uzmanlik": "Cildiye", "hastane_id": 1,
                "musaitlik": {"2025-08-10": ["16:00"], "2025-08-14": ["10:00"]}},
                {"id": 207, "adi": "Dr. Ahmet Kayhan", "uzmanlik": "Cildiye", "hastane_id": 1,
                "musaitlik": {"2025-08-15": ["10:00"], "2025-08-16": ["12:00"]}},

                {"id": 108, "adi": "Dr. Sena Doğan", "uzmanlik": "Cildiye", "hastane_id": 2,
                "musaitlik": {"2025-08-12": ["13:00"], "2025-08-15": ["13:00"]}},
                {"id": 208, "adi": "Dr. Şahin Beyazıt", "uzmanlik": "Cildiye", "hastane_id": 2,
                "musaitlik": {"2025-08-16": ["09:00"], "2025-08-17": ["15:00"]}},

                # İstanbul - Fatih (hastane_id 3 ve 4)
                {"id": 109, "adi": "Dr. Fatma Öztürk", "uzmanlik": "Kardiyoloji", "hastane_id": 3,
                "musaitlik": {"2025-08-10": ["10:00"], "2025-08-13": ["15:00"]}},
                {"id": 209, "adi": "Dr. Kerem Polat", "uzmanlik": "Kardiyoloji", "hastane_id": 3,
                "musaitlik": {"2025-08-14": ["09:00"], "2025-08-15": ["11:00"]}},

                {"id": 110, "adi": "Dr. Murat Yıldız", "uzmanlik": "Kardiyoloji", "hastane_id": 4,
                "musaitlik": {"2025-08-11": ["09:00"], "2025-08-14": ["14:00"]}},
                {"id": 210, "adi": "Dr. Esra Demirtaş", "uzmanlik": "Kardiyoloji", "hastane_id": 4,
                "musaitlik": {"2025-08-12": ["10:00"], "2025-08-16": ["13:00"]}},

                {"id": 111, "adi": "Dr. Aylin Korkmaz", "uzmanlik": "KBB", "hastane_id": 3,
                "musaitlik": {"2025-08-10": ["11:30"], "2025-08-12": ["16:00"]}},
                {"id": 211, "adi": "Dr. Hakan Yalçın", "uzmanlik": "KBB", "hastane_id": 3,
                "musaitlik": {"2025-08-13": ["09:00"], "2025-08-14": ["15:00"]}},

                {"id": 112, "adi": "Dr. Caner Bal", "uzmanlik": "KBB", "hastane_id": 4,
                "musaitlik": {"2025-08-13": ["09:00"], "2025-08-15": ["11:00"]}},
                {"id": 212, "adi": "Dr. Melis Kaptan", "uzmanlik": "KBB", "hastane_id": 4,
                "musaitlik": {"2025-08-16": ["10:00"], "2025-08-17": ["14:00"]}},

                {"id": 113, "adi": "Dr. Selma Erdem", "uzmanlik": "Nöroloji", "hastane_id": 3,
                "musaitlik": {"2025-08-11": ["14:00"], "2025-08-16": ["09:30"]}},
                {"id": 213, "adi": "Dr. Bora Yılmaz", "uzmanlik": "Nöroloji", "hastane_id": 3,
                "musaitlik": {"2025-08-17": ["10:00"], "2025-08-18": ["13:00"]}},

                {"id": 114, "adi": "Dr. Ömer Sarı", "uzmanlik": "Nöroloji", "hastane_id": 4,
                "musaitlik": {"2025-08-12": ["10:00"], "2025-08-17": ["13:00"]}},
                {"id": 214, "adi": "Dr. Gülhan Aydın", "uzmanlik": "Nöroloji", "hastane_id": 4,
                "musaitlik": {"2025-08-18": ["09:00"], "2025-08-19": ["11:00"]}},

                {"id": 115, "adi": "Dr. Ceyda Durmaz", "uzmanlik": "Cildiye", "hastane_id": 3,
                "musaitlik": {"2025-08-11": ["16:00"], "2025-08-16": ["09:30"]}},
                {"id": 215, "adi": "Dr. Berfin Kılıçarslan", "uzmanlik": "Cildiye", "hastane_id": 3,
                "musaitlik": {"2025-08-17": ["09:00"], "2025-08-18": ["13:00"]}},

                {"id": 116, "adi": "Dr. Eren Telli", "uzmanlik": "Cildiye", "hastane_id": 4,
                "musaitlik": {"2025-08-12": ["11:00"], "2025-08-17": ["13:40"]}},
                {"id": 216, "adi": "Dr. Bengisu Bağçeci", "uzmanlik": "Cildiye", "hastane_id": 4,
                "musaitlik": {"2025-08-18": ["09:30"], "2025-08-19": ["10:10"]}},

                # İzmir - Bornova (hastane_id 5 ve 6)
                {"id": 113, "adi": "Dr. Bahar Kılıç", "uzmanlik": "Kardiyoloji", "hastane_id": 5,
                "musaitlik": {"2025-08-10": ["09:30"], "2025-08-14": ["15:00"]}},
                {"id": 213, "adi": "Dr. Onur Demir", "uzmanlik": "Kardiyoloji", "hastane_id": 5,
                "musaitlik": {"2025-08-15": ["10:00"], "2025-08-16": ["14:00"]}},

                {"id": 114, "adi": "Dr. Ali Koç", "uzmanlik": "Kardiyoloji", "hastane_id": 6,
                "musaitlik": {"2025-08-11": ["10:00"], "2025-08-15": ["14:00"]}},
                {"id": 214, "adi": "Dr. Selin Polat", "uzmanlik": "Kardiyoloji", "hastane_id": 6,
                "musaitlik": {"2025-08-12": ["09:00"], "2025-08-17": ["13:00"]}},

                {"id": 115, "adi": "Dr. Funda Sezer", "uzmanlik": "KBB", "hastane_id": 5,
                "musaitlik": {"2025-08-12": ["11:00"], "2025-08-16": ["09:00"]}},
                {"id": 215, "adi": "Dr. Cem Öztürk", "uzmanlik": "KBB", "hastane_id": 5,
                "musaitlik": {"2025-08-17": ["10:00"], "2025-08-18": ["14:00"]}},

                {"id": 116, "adi": "Dr. Levent Ak", "uzmanlik": "KBB", "hastane_id": 6,
                "musaitlik": {"2025-08-13": ["13:30"], "2025-08-17": ["15:00"]}},
                {"id": 216, "adi": "Dr. Beril Kaya", "uzmanlik": "KBB", "hastane_id": 6,
                "musaitlik": {"2025-08-18": ["09:00"], "2025-08-19": ["11:00"]}},

                {"id": 117, "adi": "Dr. Yasemin Demir", "uzmanlik": "Nöroloji", "hastane_id": 5,
                "musaitlik": {"2025-08-14": ["09:00"], "2025-08-18": ["11:00"]}},
                {"id": 217, "adi": "Dr. Metin Yıldırım", "uzmanlik": "Nöroloji", "hastane_id": 5,
                "musaitlik": {"2025-08-19": ["10:00"], "2025-08-20": ["14:00"]}},

                {"id": 118, "adi": "Dr. Tolga Yaman", "uzmanlik": "Nöroloji", "hastane_id": 6,
                "musaitlik": {"2025-08-15": ["10:00"], "2025-08-19": ["14:00"]}},
                {"id": 218, "adi": "Dr. Ebru Şen", "uzmanlik": "Nöroloji", "hastane_id": 6,
                "musaitlik": {"2025-08-20": ["09:00"], "2025-08-21": ["11:00"]}},

                {"id": 119, "adi": "Dr. Ali Toksöz", "uzmanlik": "Cildiye", "hastane_id": 5,
                "musaitlik": {"2025-08-14": ["09:50"], "2025-08-18": ["11:20"]}},
                {"id": 219, "adi": "Dr. Oğuz Atay", "uzmanlik": "Cildiye", "hastane_id": 5,
                "musaitlik": {"2025-08-19": ["08:30"], "2025-08-20": ["14:30"]}},

                {"id": 120, "adi": "Dr. Nilgün Marmara", "uzmanlik": "Cildiye", "hastane_id": 6,
                "musaitlik": {"2025-08-15": ["10:00"], "2025-08-19": ["14:00"]}},
                {"id": 220, "adi": "Dr.Zeynep Bengü Şahin", "uzmanlik": "Cildiye", "hastane_id": 6,
                "musaitlik": {"2025-08-20": ["09:00"], "2025-08-21": ["11:00"]}},

                # Yozgat - Sorgun (hastane_id 7 ve 8)
                {"id": 121, "adi": "Dr. Begüm Sude Uslu", "uzmanlik": "Kardiyoloji", "hastane_id": 7,
                "musaitlik": {"2025-08-10": ["09:30"], "2025-08-14": ["15:00"]}},
                {"id": 221, "adi": "Dr. Emre Tahtalı", "uzmanlik": "Kardiyoloji", "hastane_id": 7,
                "musaitlik": {"2025-08-15": ["10:00"], "2025-08-16": ["14:00"]}},

                {"id": 122, "adi": "Dr. Ense İsment Bal", "uzmanlik": "Kardiyoloji", "hastane_id": 8,
                "musaitlik": {"2025-08-11": ["10:00"], "2025-08-15": ["14:00"]}},
                {"id": 222, "adi": "Dr. Arda Ağaçdelen", "uzmanlik": "Kardiyoloji", "hastane_id": 8,
                "musaitlik": {"2025-08-12": ["09:00"], "2025-08-17": ["13:00"]}},

                {"id": 123, "adi": "Dr. Yiğit Kaya Bağcı", "uzmanlik": "KBB", "hastane_id": 7,
                "musaitlik": {"2025-08-12": ["11:00"], "2025-08-16": ["09:00"]}},
                {"id": 223, "adi": "Dr. Ayşe Yılmaz", "uzmanlik": "KBB", "hastane_id": 7,
                "musaitlik": {"2025-08-17": ["10:00"], "2025-08-18": ["14:00"]}},

                {"id": 124, "adi": "Dr. Hatice Güçlü", "uzmanlik": "KBB", "hastane_id": 8,
                "musaitlik": {"2025-08-13": ["13:30"], "2025-08-17": ["15:00"]}},
                {"id": 224, "adi": "Dr. Bengü Durmaz", "uzmanlik": "KBB", "hastane_id": 8,
                "musaitlik": {"2025-08-18": ["09:00"], "2025-08-19": ["11:00"]}},

                {"id": 125, "adi": "Dr. Nilüfer Kasabalı", "uzmanlik": "Nöroloji", "hastane_id": 7,
                "musaitlik": {"2025-08-14": ["09:00"], "2025-08-18": ["11:00"]}},
                {"id": 225, "adi": "Dr. Ahsen Yıldırım", "uzmanlik": "Nöroloji", "hastane_id": 7,
                "musaitlik": {"2025-08-19": ["10:00"], "2025-08-20": ["14:00"]}},

                {"id": 126, "adi": "Dr. Burak Arslan", "uzmanlik": "Nöroloji", "hastane_id": 8,
                "musaitlik": {"2025-08-15": ["10:00"], "2025-08-19": ["14:00"]}},
                {"id": 226, "adi": "Dr. Erdem Şimşek", "uzmanlik": "Nöroloji", "hastane_id": 8,
                "musaitlik": {"2025-08-20": ["09:00"], "2025-08-21": ["11:00"]}},

                {"id": 127, "adi": "Dr. Gizem Çelik", "uzmanlik": "Cildiye", "hastane_id": 7,
                "musaitlik": {"2025-08-14": ["08:50", "11:30"], "2025-08-18": ["10:00", "12:00"]}},
                {"id": 227, "adi": "Dr. Azra Yıldız", "uzmanlik": "Cildiye", "hastane_id": 7,
                "musaitlik": {"2025-08-19": ["09:00"], "2025-08-20": ["12:00"]}},

                {"id": 128, "adi": "Dr. Şenel Vurvardım", "uzmanlik": "Cildiye", "hastane_id": 8,
                "musaitlik": {"2025-08-15": ["10:40"], "2025-08-19": ["15:00"]}},
                {"id": 228, "adi": "Dr. Can Cansever", "uzmanlik": "Cildiye", "hastane_id": 8,
                "musaitlik": {"2025-08-20": ["09:10"], "2025-08-21": ["14:00"]}},
            ],
            "randevular": [
                {
                    "doktor": "Dr. Gizem Çelik",
                    "hastane_adi": "Sorgun Devlet Hastanesi",
                    "poliklinik": "Cildiye",
                    "tarih": "2025-08-14",
                    "saat": "08:50"
                },
                {
                    "doktor": "Dr. Azra Yıldız",
                    "hastane_adi": "Sorgun Devlet Hastanesi",
                    "poliklinik": "Cildiye",
                    "tarih": "2025-08-19",
                    "saat": "09:00"
                }
            ]
    }