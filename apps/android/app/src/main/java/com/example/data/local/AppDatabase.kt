package com.example.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(
    entities = [
        SovereignEventEntity::class,
        CodexBookmarkEntity::class,
        ProtocolRunEntity::class,
        SourceBlockEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun sovereignEventDao(): SovereignEventDao
    abstract fun codexBookmarkDao(): CodexBookmarkDao
    abstract fun protocolRunDao(): ProtocolRunDao
    abstract fun sourceBlockDao(): SourceBlockDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "sovereign_codex.db"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}
