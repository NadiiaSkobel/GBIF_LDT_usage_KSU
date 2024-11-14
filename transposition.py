import pandas as pd

# Завантажте таблицю
file_path = 'askaniia.xlsx'  # Вкажіть шлях до вашого Excel-файлу

# Завантаження даних, враховуючи, що заголовки починаються з 10-го рядка
df = pd.read_excel(file_path, header=10)

# Перетворення даних у формат long
long_df = (
    df.melt(id_vars=df.columns[0],  # Ідентифікаційні змінні - перший стовпець
            var_name='eventID',
            value_name='organismQuantity')
    .dropna(subset=['organismQuantity'])  # Залишаємо лише непорожні комірки в колонці 'organismQuantity'
)

# Перетворення стовпця 'eventID' у рядковий тип
long_df['eventID'] = long_df['eventID'].astype(str)

# Видаляємо суфікси типу .1, .2 тощо з колонок дат у 'eventID'
long_df['eventID'] = long_df['eventID'].str.replace(r'\.\d+$', '', regex=True)

# Додаємо унікальні ідентифікатори 'occurrenceID' для кожного eventID
long_df['occurrenceID'] = long_df.groupby('eventID').cumcount() + 1
long_df['occurrenceID'] = long_df.apply(
    lambda x: f"{x['eventID']}_{x['occurrenceID']:03}", axis=1
)

# Додаємо префікс до кожного значення в стовпці 'eventID'
long_df['eventID'] = 'Askaniia_Nova_' + long_df['eventID'].astype(str)

)
# Додаємо нову колонку 'basisOfRecord' з постійним значенням 'HumanObservation' та ін.
long_df['basisOfRecord'] = 'HumanObservation'

# Зберігаємо у новий файл або виводимо результат
long_df.to_csv('long_data_format.csv', index=False)