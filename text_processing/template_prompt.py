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

    return f"""Pelajari konteks berikut : {cleaned_context} . Tolong bantu saya menjawab pertanyaan berikut : {question}.Jawab dengan menjelaskan kembali kepada saya dengan komprehensif serta dengan kata-kata anda sendiri tanpa perlu menjelaskan yang menurut anda tidak relevan. Berikan penjelasan atau mungkin fakta berdasarkan konteks tersebut yang bersifat akurat dan dapat saya percaya.
Jika konteks yang saya berikan kosong, coba jawab pertanyaan yang saya berikan tetapi tetap dengan syarat: Jika anda ragu menjawabnya lebih baik bertanya kembali atau menolak menjawab dengan halus. """