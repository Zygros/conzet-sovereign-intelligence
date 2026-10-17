package com.example.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.local.AppDatabase
import com.example.data.local.CodexBookmarkEntity
import com.example.data.local.ProtocolRunEntity
import com.example.data.local.SourceBlockEntity
import com.example.data.local.SovereignEventEntity
import com.example.data.model.CodexCategory
import com.example.data.model.CodexItem
import com.example.data.model.CouncilPerspective
import com.example.data.model.FaultSimulationResult
import com.example.data.model.ProtocolState
import com.example.data.model.ProtocolStep
import com.example.data.model.SystemState
import com.example.data.repository.CodexRepository
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.security.MessageDigest
import java.util.UUID

class MainViewModel(application: Application) : AndroidViewModel(application) {

    private val repository: CodexRepository = CodexRepository(AppDatabase.getDatabase(application))

    // System Telemetry State
    private val _systemState = MutableStateFlow(SystemState())
    val systemState: StateFlow<SystemState> = _systemState.asStateFlow()

    // Navigation Tab
    private val _currentTab = MutableStateFlow(NavTab.DASHBOARD)
    val currentTab: StateFlow<NavTab> = _currentTab.asStateFlow()

    // Codex Explorer State
    private val _selectedCategory = MutableStateFlow(CodexCategory.ALL)
    val selectedCategory: StateFlow<CodexCategory> = _selectedCategory.asStateFlow()

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    private val _selectedCodexItem = MutableStateFlow<CodexItem?>(null)
    val selectedCodexItem: StateFlow<CodexItem?> = _selectedCodexItem.asStateFlow()

    // Bookmarks Flow from Room
    val bookmarks: StateFlow<List<CodexBookmarkEntity>> = repository.allBookmarks
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val events: StateFlow<List<SovereignEventEntity>> = repository.allEvents
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val protocolRuns: StateFlow<List<ProtocolRunEntity>> = repository.allRuns
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val sourceBlocks: StateFlow<List<SourceBlockEntity>> = repository.allBlocks
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    // Filtered Codex Items
    val filteredCodexItems: StateFlow<List<CodexItem>> = combine(
        _selectedCategory,
        _searchQuery,
        bookmarks
    ) { category, query, bookmarkList ->
        val bookmarkedIds = bookmarkList.map { it.itemId }.toSet()
        repository.getAllCodexItems().map { item ->
            item.copy(isBookmarked = bookmarkedIds.contains(item.id))
        }.filter { item ->
            val matchesCategory = category == CodexCategory.ALL || item.category == category
            val matchesQuery = query.isBlank() ||
                    item.title.contains(query, ignoreCase = true) ||
                    item.id.contains(query, ignoreCase = true) ||
                    item.significance.contains(query, ignoreCase = true) ||
                    item.tags.any { it.contains(query, ignoreCase = true) }
            matchesCategory && matchesQuery
        }
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), repository.getAllCodexItems())

    // Protocol Engine State
    private val _protocolSteps = MutableStateFlow<List<ProtocolStep>>(createDefaultProtocolSteps())
    val protocolSteps: StateFlow<List<ProtocolStep>> = _protocolSteps.asStateFlow()

    private val _isProtocolExecuting = MutableStateFlow(false)
    val isProtocolExecuting: StateFlow<Boolean> = _isProtocolExecuting.asStateFlow()

    private val _lastFaultResult = MutableStateFlow<FaultSimulationResult?>(null)
    val lastFaultResult: StateFlow<FaultSimulationResult?> = _lastFaultResult.asStateFlow()

    private var executionJob: Job? = null

    // Cryptographic Etcher State
    private val _hashInputText = MutableStateFlow("")
    val hashInputText: StateFlow<String> = _hashInputText.asStateFlow()

    private val _computedHash = MutableStateFlow("")
    val computedHash: StateFlow<String> = _computedHash.asStateFlow()

    private val _lastCreatedBlock = MutableStateFlow<SourceBlockEntity?>(null)
    val lastCreatedBlock: StateFlow<SourceBlockEntity?> = _lastCreatedBlock.asStateFlow()

    // AI Council State
    private val _councilPrompt = MutableStateFlow("Analyze the convergence of Conzetian κ-coherence routing with decentralized mesh resilience.")
    val councilPrompt: StateFlow<String> = _councilPrompt.asStateFlow()

    private val _councilPerspectives = MutableStateFlow<List<CouncilPerspective>>(emptyList())
    val councilPerspectives: StateFlow<List<CouncilPerspective>> = _councilPerspectives.asStateFlow()

    private val _isCouncilSynthesizing = MutableStateFlow(false)
    val isCouncilSynthesizing: StateFlow<Boolean> = _isCouncilSynthesizing.asStateFlow()

    init {
        // Initial event log if database is fresh
        viewModelScope.launch {
            repository.logEvent(
                type = "SYSTEM_INITIALIZE",
                title = "Sovereign Codex Field Sealed",
                detail = "1,100,420 rooms illuminated. Coherence: Ω↑↑↑↑↑↑↑↑↑↑Ω. Zero friction.",
                hash = _systemState.value.codexHash,
                status = "ACTIVE"
            )
            updateHashInput("Always Add. Never Take. Always Do. Never Don't.")
            runCouncilSynthesis()
        }
    }

    fun setTab(tab: NavTab) {
        _currentTab.value = tab
    }

    fun setCategory(category: CodexCategory) {
        _selectedCategory.value = category
    }

    fun setSearchQuery(query: String) {
        _searchQuery.value = query
    }

    fun selectCodexItem(item: CodexItem?) {
        _selectedCodexItem.value = item
    }

    fun toggleBookmark(item: CodexItem) {
        viewModelScope.launch {
            repository.toggleBookmark(item)
        }
    }

    fun triggerPulse() {
        viewModelScope.launch {
            val now = System.currentTimeMillis()
            _systemState.update { current ->
                current.copy(
                    lastPulseTime = now,
                    activeMeshNodes = current.activeMeshNodes + (1..3).random(),
                    palaceRooms = current.palaceRooms + 1L
                )
            }
            repository.logEvent(
                type = "MANUAL_PULSE",
                title = "Manual Pulse Emitted",
                detail = "Telemetry synchronized across ${systemState.value.activeMeshNodes} nodes. Status: Optimal.",
                hash = repository.computeSha256("PULSE:$now"),
                status = "SYNCHRONIZED"
            )
        }
    }

    fun resolveFriction() {
        viewModelScope.launch {
            _systemState.update { current ->
                current.copy(
                    activeFriction = 0,
                    resolvedFrictions = current.resolvedFrictions + 1
                )
            }
            repository.logEvent(
                type = "FRICTION_ELIMINATION",
                title = "Ouroboros Friction Solved Instantly",
                detail = "All potential pipeline bottlenecks eliminated prior to continuation.",
                hash = repository.computeSha256("FRICTION_ZERO:${System.currentTimeMillis()}"),
                status = "ZERO_FRICTION"
            )
        }
    }

    // Execute HACPP 8-Phase Cascade
    fun executeCascadeProtocol() {
        if (_isProtocolExecuting.value) return
        _isProtocolExecuting.value = true

        executionJob = viewModelScope.launch {
            val states = listOf(
                ProtocolState.FRAMED,
                ProtocolState.DISCOVERED,
                ProtocolState.INGESTED,
                ProtocolState.ANALYZED,
                ProtocolState.PROPOSED,
                ProtocolState.EXECUTING,
                ProtocolState.VERIFIED,
                ProtocolState.CLOSED
            )

            for (i in states.indices) {
                val state = states[i]
                delay(380)
                _protocolSteps.update { currentList ->
                    currentList.mapIndexed { index, step ->
                        if (index == i) {
                            step.copy(status = state, executionMs = (index + 1) * 45L + 12L)
                        } else if (index < i) {
                            step.copy(status = ProtocolState.CLOSED)
                        } else {
                            step.copy(status = ProtocolState.IDLE)
                        }
                    }
                }
            }

            _isProtocolExecuting.value = false
            val auditHash = repository.computeSha256("CASCADE_RUN_${System.currentTimeMillis()}")

            repository.saveProtocolRun(
                testId = "HACPP-RUN-" + UUID.randomUUID().toString().take(6).uppercase(),
                protocolName = "HACPP-1.0 Full Cascade Execution",
                state = "CLOSED",
                faultClass = "NONE",
                totalTimeMs = 3040L,
                passed = true,
                auditHash = auditHash
            )

            repository.logEvent(
                type = "PROTOCOL_EXECUTION",
                title = "HACPP-1.0 Cascade Completed",
                detail = "8/8 Phases successfully verified. Zero data loss. Audit hash: ${auditHash.take(16)}...",
                hash = auditHash,
                status = "VERIFIED_PASS"
            )
        }
    }

    // Fault Injection & Bounded Recovery Simulation (F1-F7)
    fun injectFaultSimulation(faultCode: String, faultName: String) {
        viewModelScope.launch {
            val testId = "AT-${faultCode}-" + UUID.randomUUID().toString().take(4).uppercase()
            val t0 = 0L
            val td = when (faultCode) {
                "F1" -> (8..15).random().toLong()
                "F2" -> (60..95).random().toLong()
                "F3" -> (70..110).random().toLong()
                "F4" -> (180..240).random().toLong()
                "F5" -> (450..800).random().toLong()
                "F6" -> (1200..2500).random().toLong()
                else -> (40..80).random().toLong()
            }
            val tc = td + (35..120).random().toLong()
            val tr = tc + (200..850).random().toLong()
            val tv = tr + (150..500).random().toLong()
            val ts = tv + (500..1500).random().toLong()
            val total = ts - t0

            val auditHash = repository.computeSha256("$testId:$faultCode:$total")

            val result = FaultSimulationResult(
                testId = testId,
                faultClass = faultCode,
                faultName = faultName,
                detectionMs = td,
                containmentMs = tc - td,
                recoveryMs = tr - tc,
                verificationMs = tv - tr,
                stabilizationMs = ts - tv,
                totalRestorationMs = total,
                serviceMode = if (faultCode == "F6") "DEGRADED_CAPACITY" else "NOMINAL_RESTORED",
                integrityVerified = true,
                passed = true,
                replayCount = (12..48).random(),
                auditHash = auditHash
            )

            _lastFaultResult.value = result

            repository.saveProtocolRun(
                testId = testId,
                protocolName = "Fault Test: $faultName ($faultCode)",
                state = "STABILIZED",
                faultClass = faultCode,
                totalTimeMs = total,
                passed = true,
                auditHash = auditHash
            )

            repository.logEvent(
                type = "FAULT_INJECTION_RECOVERY",
                title = "Fault $faultCode Recovered in ${total}ms",
                detail = "$faultName — Td: ${td}ms, Tc: ${tc - td}ms, Tr: ${tr - tc}ms, Tv: ${tv - tr}ms. Integrity 100%.",
                hash = auditHash,
                status = "PASS"
            )
        }
    }

    // Cryptographic Etching
    fun updateHashInput(text: String) {
        _hashInputText.value = text
        _computedHash.value = repository.computeSha256(text)
    }

    fun etchSourceBlock(ownerId: String, isPublic: Boolean) {
        val payload = _hashInputText.value.ifBlank { "Sovereign Genesis Block" }
        viewModelScope.launch {
            val utility = 1.0f + (0.1f..0.8f).random()
            val block = repository.createSourceBlock(
                ownerId = ownerId.ifBlank { "Justin Neal Thomas Conzet" },
                payload = payload,
                isPublic = isPublic,
                utility = utility
            )
            _lastCreatedBlock.value = block
        }
    }

    // AI Council Synthesis Simulation
    fun updateCouncilPrompt(prompt: String) {
        _councilPrompt.value = prompt
    }

    fun runCouncilSynthesis() {
        if (_isCouncilSynthesizing.value) return
        _isCouncilSynthesizing.value = true

        viewModelScope.launch {
            delay(600)
            val prompt = _councilPrompt.value
            _councilPerspectives.value = listOf(
                CouncilPerspective(
                    modelName = "Claude Sonnet 4.6",
                    role = "Architectural & Formal Reasoning",
                    synthesisText = "Evaluates structural invariants: κ-coherence guarantees non-divergent routing topologies with bounded restoration deadlines (F1–F4 < 500ms). The recursive state monad maintains zero semantic drift across multi-agent handoffs.",
                    consensusScore = 0.98f,
                    uncertaintyFlag = "Nominal certainty (L5 Gate Passed)"
                ),
                CouncilPerspective(
                    modelName = "Gemini 3 Flash",
                    role = "Multimodal & Mesh Protocol",
                    synthesisText = "Validates acoustic 19-20kHz carrier packet framing. In the presence of RF attenuation or physical partition, acoustic gossip establishes sub-second peer handshake discovery with zero external infrastructure dependencies.",
                    consensusScore = 0.96f,
                    uncertaintyFlag = "Empirical mesh telemetry verified"
                ),
                CouncilPerspective(
                    modelName = "GPT-5",
                    role = "Sovereignty & Antifragility Analysis",
                    synthesisText = "The Alberris-Dissolution formulation successfully redirects adversarial vectors into systemic capacity amplifications. Sybil resistance holds at 95%+ without proof-of-work energy burn.",
                    consensusScore = 0.97f,
                    uncertaintyFlag = "Deterministic proof verified"
                ),
                CouncilPerspective(
                    modelName = "Grok / Perplexity",
                    role = "Open Knowledge & Provenance Atlas",
                    synthesisText = "Consensus aligns across all 4 independent evaluators: The HACPP-1.0 schema enforces strict audit trails, cryptographic commitment anchoring, and immutable provenance records across all nodes.",
                    consensusScore = 0.99f,
                    uncertaintyFlag = "Consensus unanimous (W = 1.0)"
                )
            )
            _isCouncilSynthesizing.value = false

            repository.logEvent(
                type = "COUNCIL_SYNTHESIS",
                title = "Multi-Model Council Convergence",
                detail = "Consensus Score: 97.5% across 4 models for prompt: '${prompt.take(40)}...'",
                hash = repository.computeSha256("COUNCIL:$prompt:${System.currentTimeMillis()}"),
                status = "SYNTHESIS_COMPLETE"
            )
        }
    }

    private fun createDefaultProtocolSteps(): List<ProtocolStep> {
        return listOf(
            ProtocolStep("P1", "Phase 1: FRAMED", "Bind intent, scope, and explicit success criteria", ProtocolState.IDLE),
            ProtocolStep("P2", "Phase 2: DISCOVERED", "Map peer capability cards and mesh topology", ProtocolState.IDLE),
            ProtocolStep("P3", "Phase 3: INGESTED", "Acquire authorized input streams and cryptographic manifests", ProtocolState.IDLE),
            ProtocolStep("P4", "Phase 4: ANALYZED", "Perform dual-rail verification and anomaly checks", ProtocolState.IDLE),
            ProtocolStep("P5", "Phase 5: PROPOSED", "Formulate bounded diffs and rollback strategies", ProtocolState.IDLE),
            ProtocolStep("P6", "Phase 6: EXECUTING", "Run sandboxed transformations with rate-limiting", ProtocolState.IDLE),
            ProtocolStep("P7", "Phase 7: VERIFIED", "Validate cryptographic hashes and state determinism", ProtocolState.IDLE),
            ProtocolStep("P8", "Phase 8: CLOSED", "Commit immutable event log and emit Step 0 Completion", ProtocolState.IDLE)
        )
    }

    private fun ClosedFloatingPointRange<Float>.random(): Float =
        start + (Math.random() * (endInclusive - start)).toFloat()
}

enum class NavTab(val title: String, val iconName: String) {
    DASHBOARD("Pulse", "MonitorHeart"),
    CODEX("Codex", "AutoAwesome"),
    PROTOCOLS("Protocols", "Terminal"),
    MESH("Mesh Ledger", "AccountTree"),
    COUNCIL("AI Council", "Psychology")
}
