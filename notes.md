
# Notes — Simple RAG Refactor

## Overview

Refactor ini mengubah simple RAG dari satu file menjadi desain berbasis **OOP**. Tujuannya membuat kode lebih terstruktur tanpa mengubah perilaku sistem secara fungsional.

## Design Decisions

* **OOP-based Components**

  * `EmbeddingService`: generate embedding sederhana
  * `DocumentStore`: simpan & cari dokumen (Qdrant / in-memory fallback)
  * `RagWorkflow`: alur retrieve → answer
  * `Routes`: endpoint API (`/add`, `/ask`, `/status`)
* **Clear Responsibility**

  * Setiap class fokus pada satu tugas.
  * Mengurangi campur aduk logika API, storage, dan workflow yang sebelumnya ada di satu file.

## Trade-off

* **Lebih Banyak File**

  * Untuk demo kecil, satu file lebih cepat dipahami.
  * Namun pendekatan OOP dipilih karena alur tetap sama, tapi kode lebih rapi dan siap berkembang (misalnya ganti embedding dummy dengan model nyata).

## Maintainability

* **Isolated Changes**

  * Perubahan pada satu class tidak berdampak ke bagian lain.
* **Easier Testing**

  * Tiap komponen bisa diuji terpisah tanpa menjalankan full API.
* **Closer to Production Pattern**

  * Struktur lebih mendekati praktik umum pada implementasi RAG di dunia nyata.

---
