package com.example.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "sovereign_events")
data class SovereignEventEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val timestamp: Long,
    val type: String,
    val title: String,
    val detail: String,
    val hash: String,
    val status: String
)

@Entity(tableName = "codex_bookmarks")
data class CodexBookmarkEntity(
    @PrimaryKey val itemId: String,
    val title: String,
    val category: String,
    val tier: String,
    val timestamp: Long
)

@Entity(tableName = "protocol_runs")
data class ProtocolRunEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val testId: String,
    val protocolName: String,
    val state: String,
    val faultClass: String,
    val totalTimeMs: Long,
    val passed: Boolean,
    val timestamp: Long,
    val auditHash: String
)

@Entity(tableName = "source_blocks")
data class SourceBlockEntity(
    @PrimaryKey val blockId: String,
    val ownerId: String,
    val publicCommitment: String,
    val createdAt: Long,
    val utility: Float,
    val isPublic: Boolean,
    val payloadPreview: String
)
