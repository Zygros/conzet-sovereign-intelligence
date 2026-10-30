package com.example.ui.components

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.widget.Toast
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.BookmarkBorder
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Functions
import androidx.compose.material.icons.filled.Shield
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.model.CodexItem
import com.example.ui.theme.AmethystViolet
import com.example.ui.theme.EmeraldRestore
import com.example.ui.theme.OutlineDark
import com.example.ui.theme.QuantumCyan
import com.example.ui.theme.SovereignGold
import com.example.ui.theme.SurfaceDark
import com.example.ui.theme.SurfaceElevatedDark
import com.example.ui.theme.SurfaceVariantDark
import com.example.ui.theme.TextPrimaryDark
import com.example.ui.theme.TextSecondaryDark
import com.example.ui.theme.TextTertiaryDark

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun CodexDetailModal(
    item: CodexItem,
    onDismiss: () -> Unit,
    onToggleBookmark: () -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val context = LocalContext.current

    val tierColor = when {
        item.tier.contains("Cosmic", ignoreCase = true) -> SovereignGold
        item.tier.contains("Omega", ignoreCase = true) -> AmethystViolet
        item.tier.contains("Transcendent", ignoreCase = true) -> QuantumCyan
        item.tier.contains("Absolute", ignoreCase = true) -> EmeraldRestore
        else -> SovereignGold
    }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        containerColor = SurfaceDark,
        tonalElevation = 8.dp
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp)
                .padding(bottom = 32.dp)
                .verticalScroll(rememberScrollState())
        ) {
            // Header Row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Surface(
                        shape = RoundedCornerShape(8.dp),
                        color = tierColor.copy(alpha = 0.2f),
                        border = BorderStroke(1.dp, tierColor)
                    ) {
                        Text(
                            text = item.id,
                            style = MaterialTheme.typography.titleSmall.copy(
                                fontWeight = FontWeight.Black,
                                fontSize = 13.sp
                            ),
                            color = tierColor,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                        )
                    }

                    Spacer(modifier = Modifier.width(10.dp))

                    Text(
                        text = item.tier,
                        style = MaterialTheme.typography.labelMedium.copy(
                            fontWeight = FontWeight.Bold,
                            fontSize = 13.sp
                        ),
                        color = TextSecondaryDark
                    )
                }

                Row {
                    IconButton(
                        onClick = onToggleBookmark,
                        modifier = Modifier.testTag("modal_bookmark_button")
                    ) {
                        Icon(
                            imageVector = if (item.isBookmarked) Icons.Default.Bookmark else Icons.Default.BookmarkBorder,
                            contentDescription = "Bookmark",
                            tint = if (item.isBookmarked) SovereignGold else TextTertiaryDark
                        )
                    }

                    IconButton(
                        onClick = onDismiss,
                        modifier = Modifier.testTag("modal_close_button")
                    ) {
                        Icon(
                            imageVector = Icons.Default.Close,
                            contentDescription = "Close",
                            tint = TextSecondaryDark
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Title
            Text(
                text = item.title,
                style = MaterialTheme.typography.headlineSmall.copy(
                    fontWeight = FontWeight.Black,
                    fontSize = 22.sp,
                    letterSpacing = (-0.5).sp
                ),
                color = TextPrimaryDark
            )

            Spacer(modifier = Modifier.height(8.dp))

            // Rarity & Category Banner
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = SurfaceVariantDark,
                    border = BorderStroke(0.5.dp, OutlineDark)
                ) {
                    Text(
                        text = "Rarity: ${item.rarity}",
                        style = MaterialTheme.typography.labelSmall.copy(
                            fontSize = 11.sp,
                            fontWeight = FontWeight.SemiBold
                        ),
                        color = SovereignGold,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                    )
                }

                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = SurfaceVariantDark,
                    border = BorderStroke(0.5.dp, OutlineDark)
                ) {
                    Text(
                        text = item.category.displayName,
                        style = MaterialTheme.typography.labelSmall.copy(
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Medium
                        ),
                        color = QuantumCyan,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(20.dp))

            // Significance Section
            Text(
                text = "ONTOLOGICAL SIGNIFICANCE",
                style = MaterialTheme.typography.labelSmall.copy(
                    fontWeight = FontWeight.Black,
                    letterSpacing = 1.sp,
                    fontSize = 11.sp
                ),
                color = TextTertiaryDark
            )

            Spacer(modifier = Modifier.height(6.dp))

            Surface(
                shape = RoundedCornerShape(12.dp),
                color = SurfaceElevatedDark,
                border = BorderStroke(1.dp, OutlineDark)
            ) {
                Text(
                    text = item.significance,
                    style = MaterialTheme.typography.bodyMedium.copy(
                        fontSize = 14.sp,
                        lineHeight = 22.sp
                    ),
                    color = TextPrimaryDark,
                    modifier = Modifier.padding(16.dp)
                )
            }

            // Formula / Equation Section
            if (item.equationOrDetail.isNotBlank()) {
                Spacer(modifier = Modifier.height(18.dp))

                Text(
                    text = "FIELD EQUATION / FORMAL PROOF",
                    style = MaterialTheme.typography.labelSmall.copy(
                        fontWeight = FontWeight.Black,
                        letterSpacing = 1.sp,
                        fontSize = 11.sp
                    ),
                    color = TextTertiaryDark
                )

                Spacer(modifier = Modifier.height(6.dp))

                Surface(
                    shape = RoundedCornerShape(12.dp),
                    color = Color.Black.copy(alpha = 0.6f),
                    border = BorderStroke(1.dp, QuantumCyan.copy(alpha = 0.4f))
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    imageVector = Icons.Default.Functions,
                                    contentDescription = null,
                                    tint = QuantumCyan,
                                    modifier = Modifier.size(16.dp)
                                )
                                Spacer(modifier = Modifier.width(6.dp))
                                Text(
                                    text = "Mathematical Specification",
                                    style = MaterialTheme.typography.labelSmall.copy(
                                        fontSize = 11.sp,
                                        fontWeight = FontWeight.SemiBold
                                    ),
                                    color = QuantumCyan
                                )
                            }

                            IconButton(
                                onClick = {
                                    val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                                    clipboard.setPrimaryClip(ClipData.newPlainText("Equation", item.equationOrDetail))
                                    Toast.makeText(context, "Equation copied to clipboard", Toast.LENGTH_SHORT).show()
                                },
                                modifier = Modifier.size(28.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Default.ContentCopy,
                                    contentDescription = "Copy Equation",
                                    tint = QuantumCyan,
                                    modifier = Modifier.size(15.dp)
                                )
                            }
                        }

                        Spacer(modifier = Modifier.height(8.dp))

                        Text(
                            text = item.equationOrDetail,
                            style = MaterialTheme.typography.bodyMedium.copy(
                                fontFamily = FontFamily.Monospace,
                                fontSize = 13.sp,
                                lineHeight = 19.sp,
                                fontWeight = FontWeight.Medium
                            ),
                            color = Color(0xFFE0F2FE)
                        )
                    }
                }
            }

            // Tags
            if (item.tags.isNotEmpty()) {
                Spacer(modifier = Modifier.height(18.dp))
                Text(
                    text = "TAGS & PROVENANCE CLUSTERS",
                    style = MaterialTheme.typography.labelSmall.copy(
                        fontWeight = FontWeight.Black,
                        letterSpacing = 1.sp,
                        fontSize = 11.sp
                    ),
                    color = TextTertiaryDark
                )

                Spacer(modifier = Modifier.height(8.dp))

                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    item.tags.forEach { tag ->
                        Surface(
                            shape = RoundedCornerShape(16.dp),
                            color = SurfaceVariantDark,
                            border = BorderStroke(0.5.dp, OutlineDark)
                        ) {
                            Text(
                                text = "#$tag",
                                style = MaterialTheme.typography.labelSmall.copy(
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Medium
                                ),
                                color = TextSecondaryDark,
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                            )
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Action Buttons
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                OutlinedButton(
                    onClick = {
                        val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                        val fullSummary = "${item.id} — ${item.title}\nTier: ${item.tier}\nRarity: ${item.rarity}\n${item.significance}\nEquation: ${item.equationOrDetail}"
                        clipboard.setPrimaryClip(ClipData.newPlainText("Codex Item", fullSummary))
                        Toast.makeText(context, "Full specification copied", Toast.LENGTH_SHORT).show()
                    },
                    modifier = Modifier
                        .weight(1f)
                        .height(48.dp)
                        .testTag("copy_spec_button"),
                    shape = RoundedCornerShape(12.dp),
                    border = BorderStroke(1.dp, OutlineDark),
                    colors = ButtonDefaults.outlinedButtonColors(
                        contentColor = TextPrimaryDark
                    )
                ) {
                    Icon(
                        imageVector = Icons.Default.ContentCopy,
                        contentDescription = null,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Copy Spec", fontSize = 13.sp)
                }

                Button(
                    onClick = onDismiss,
                    modifier = Modifier
                        .weight(1f)
                        .height(48.dp)
                        .testTag("confirm_seal_button"),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = SovereignGold,
                        contentColor = Color.Black
                    )
                ) {
                    Icon(
                        imageVector = Icons.Default.Shield,
                        contentDescription = null,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Sealed in Field", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                }
            }
        }
    }
}
