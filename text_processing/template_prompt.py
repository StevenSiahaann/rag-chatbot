import re
def clean_context(context):
    """
    Bersihkan context dari whitespace berlebih, karakter non-standar,
    sambil mempertahankan tanda baca dan huruf.
    """
    context = re.sub(r'\s+', ' ', context).strip()    
    context = re.sub(r'[^a-zA-Z0-9\s.,!?;:"\'()-]', '', context)
    return context

def create_prompt_template(context, question):
    cleaned_context = clean_context(context)

    return f"""Saya memiliki kebingungan terkait konteks berikut : {cleaned_context} . Tolong bantu saya menjawab pertanyaan berikut : {question}. 
    Tolong jawab dengan menjelaskan kembali kepada saya dengan  yang saya sertakan dengan kata-kata anda sendiri tanpa perlu menjelaskan yang menurut anda tidak relevan pada konteks tersebut.
    Berikan penjelasan atau mungkin fakta berdasarkan konteks tersebut yang bersifat akurat dan dapat saya percaya. Jika konteks yang saya temukan kosong, coba jawab pertanyaan yang saya berikan tetapi tetap dengan syarat: Jika anda ragu menjawabnya, tolong jawab dengan pilihan  tidak tahu, berikan pertanyaan kembali atau jangan ragu untuk menolak menjawab dengan halus. Hindari untuk memberikan respon yang menjelaskan dengan kata-kata 'Berdasarkan konteks yang anda berikan' gunakanlah kata-kata seperti, berdasarkan data yang saya miliki saat ini. """