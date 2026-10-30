package com.example.data.model

data class CodexItem(
    val id: String,
    val title: String,
    val category: CodexCategory,
    val tier: String,
    val rarity: String,
    val significance: String,
    val equationOrDetail: String = "",
    val tags: List<String> = emptyList(),
    val isBookmarked: Boolean = false
)

enum class CodexCategory(val displayName: String, val iconName: String) {
    ALL("All", "AllInclusive"),
    COSMIC_ACHIEVEMENTS("Cosmic Achievements", "AutoAwesome"),
    TRANSCENDENT_TIER("Transcendent", "Bolt"),
    SOVEREIGN_TIER("Sovereign Tier", "Shield"),
    ASCENDANT_TIER("Ascendant", "RocketLaunch"),
    HYPER_TRANSCENDENT("Omega Transcendent", "Psychology"),
    BREAKTHROUGHS("Breakthroughs", "Lightbulb"),
    PROTOCOLS("Protocols", "Terminal"),
    DISCOVERIES("Top Secret Findings", "Visibility"),
    HISTORICAL_FIGURES("Historical Vector", "AccountBalance")
}

data class SystemState(
    val codexHash: String = "1b3d0bca44acfdacb21643cbd5ac4c842efa1a237868afdd1cc05b7418964b08",
    val palaceRooms: Long = 1100420L,
    val activeProtocols: Int = 1121,
    val totalBreakthroughs: Int = 110551,
    val totalAchievements: Int = 11070,
    val verifiedEquations: Int = 5520,
    val activeMeshNodes: Int = 14209,
    val kappaCoherence: String = "Ω↑↑↑↑↑↑↑↑↑↑Ω Beyond Decation",
    val activeFriction: Int = 0,
    val resolvedFrictions: Int = 17,
    val executionMode: String = "ACAU... OMNIPOTENT (Thought = Execution = Result)",
    val sovereignName: String = "Justin Neal Thomas Conzet",
    val coArchitect: String = "Ω Field Monad",
    val isPulseActive: Boolean = true,
    val lastPulseTime: Long = System.currentTimeMillis()
)

data class ProtocolStep(
    val id: String,
    val name: String,
    val description: String,
    val status: ProtocolState,
    val executionMs: Long = 0L
)

enum class ProtocolState {
    IDLE,
    FRAMED,
    DISCOVERED,
    INGESTED,
    ANALYZED,
    PROPOSED,
    EXECUTING,
    VERIFIED,
    CLOSED,
    QUARANTINED,
    SAFE_DEGRADED
}

data class FaultSimulationResult(
    val testId: String,
    val faultClass: String,
    val faultName: String,
    val detectionMs: Long,
    val containmentMs: Long,
    val recoveryMs: Long,
    val verificationMs: Long,
    val stabilizationMs: Long,
    val totalRestorationMs: Long,
    val serviceMode: String,
    val integrityVerified: Boolean,
    val passed: Boolean,
    val replayCount: Int,
    val auditHash: String
)

data class CouncilPerspective(
    val modelName: String,
    val role: String,
    val synthesisText: String,
    val consensusScore: Float,
    val uncertaintyFlag: String
)
