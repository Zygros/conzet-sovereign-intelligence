package com.example.data.local

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface SovereignEventDao {
    @Query("SELECT * FROM sovereign_events ORDER BY timestamp DESC")
    fun getAllEvents(): Flow<List<SovereignEventEntity>>

    @Query("SELECT * FROM sovereign_events ORDER BY timestamp DESC LIMIT :limit")
    fun getRecentEvents(limit: Int): Flow<List<SovereignEventEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertEvent(event: SovereignEventEntity)

    @Query("DELETE FROM sovereign_events")
    suspend fun clearEvents()
}

@Dao
interface CodexBookmarkDao {
    @Query("SELECT * FROM codex_bookmarks ORDER BY timestamp DESC")
    fun getAllBookmarks(): Flow<List<CodexBookmarkEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertBookmark(bookmark: CodexBookmarkEntity)

    @Delete
    suspend fun deleteBookmark(bookmark: CodexBookmarkEntity)

    @Query("DELETE FROM codex_bookmarks WHERE itemId = :itemId")
    suspend fun deleteByItemId(itemId: String)

    @Query("SELECT EXISTS(SELECT 1 FROM codex_bookmarks WHERE itemId = :itemId)")
    fun isBookmarked(itemId: String): Flow<Boolean>
}

@Dao
interface ProtocolRunDao {
    @Query("SELECT * FROM protocol_runs ORDER BY timestamp DESC")
    fun getAllRuns(): Flow<List<ProtocolRunEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertRun(run: ProtocolRunEntity)

    @Query("DELETE FROM protocol_runs")
    suspend fun clearRuns()
}

@Dao
interface SourceBlockDao {
    @Query("SELECT * FROM source_blocks ORDER BY createdAt DESC")
    fun getAllBlocks(): Flow<List<SourceBlockEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertBlock(block: SourceBlockEntity)

    @Query("SELECT COUNT(*) FROM source_blocks")
    fun getBlockCount(): Flow<Int>
}
