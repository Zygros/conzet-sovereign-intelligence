package com.example.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.BookmarkBorder
import androidx.compose.material.icons.filled.Functions
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
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
import com.example.ui.theme.SurfaceVariantDark
import com.example.ui.theme.TextPrimaryDark
import com.example.ui.theme.TextSecondaryDark
import com.example.ui.theme.TextTertiaryDark

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun CodexItemCard(
    item: CodexItem,
    onClick: () -> Unit,
    onToggleBookmark: () -> Unit,
    modifier: Modifier = Modifier
) {
    val tierColor = when {
        item.tier.contains("Cosmic", ignoreCase = true) -> SovereignGold
        item.tier.contains("Omega", ignoreCase = true) -> AmethystViolet
        item.tier.contains("Transcendent", ignoreCase = true) -> QuantumCyan
        item.tier.contains("Absolute", ignoreCase = true) -> EmeraldRestore
        else -> SovereignGold
    }

    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .testTag("codex_item_${item.id}"),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = SurfaceVariantDark
        ),
        border = BorderStroke(1.dp, OutlineDark)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            // Header Row: ID, Tier Badge, Bookmark
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Surface(
                        shape = RoundedCornerShape(6.dp),
                        color = tierColor.copy(alpha = 0.15f),
                        border = BorderStroke(0.5.dp, tierColor.copy(alpha = 0.5f))
                    ) {
                        Text(
                            text = item.id,
                            style = MaterialTheme.typography.labelSmall.copy(
                                fontWeight = FontWeight.Black,
                                fontSize = 11.sp
                            ),
                            color = tierColor,
                            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                        )
                    }

                    Spacer(modifier = Modifier.width(8.dp))

                    Text(
                        text = item.tier,
                        style = MaterialTheme.typography.labelSmall.copy(
                            fontWeight = FontWeight.SemiBold,
                            fontSize = 11.sp
                        ),
                        color = TextSecondaryDark
                    )
                }

                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = item.rarity,
                        style = MaterialTheme.typography.labelSmall.copy(
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Medium
                        ),
                        color = SovereignGold.copy(alpha = 0.9f)
                    )

                    IconButton(
                        onClick = onToggleBookmark,
                        modifier = Modifier
                            .size(32.dp)
                            .testTag("bookmark_${item.id}")
                    ) {
                        Icon(
                            imageVector = if (item.isBookmarked) Icons.Default.Bookmark else Icons.Default.BookmarkBorder,
                            contentDescription = "Bookmark",
                            tint = if (item.isBookmarked) SovereignGold else TextTertiaryDark,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Title
            Text(
                text = item.title,
                style = MaterialTheme.typography.titleMedium.copy(
                    fontWeight = FontWeight.Bold,
                    fontSize = 16.sp,
                    letterSpacing = (-0.2).sp
                ),
                color = TextPrimaryDark
            )

            Spacer(modifier = Modifier.height(6.dp))

            // Significance
            Text(
                text = item.significance,
                style = MaterialTheme.typography.bodySmall.copy(
                    fontSize = 12.5.sp,
                    lineHeight = 18.sp
                ),
                color = TextSecondaryDark,
                maxLines = 3
            )

            // Equation if available
            if (item.equationOrDetail.isNotBlank()) {
                Spacer(modifier = Modifier.height(10.dp))
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = Color.Black.copy(alpha = 0.4f),
                    border = BorderStroke(0.5.dp, OutlineDark)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 10.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Default.Functions,
                            contentDescription = null,
                            tint = QuantumCyan,
                            modifier = Modifier.size(14.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = item.equationOrDetail,
                            style = MaterialTheme.typography.labelSmall.copy(
                                fontFamily = FontFamily.Monospace,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Medium
                            ),
                            color = QuantumCyan,
                            maxLines = 1
                        )
                    }
                }
            }

            // Tags
            if (item.tags.isNotEmpty()) {
                Spacer(modifier = Modifier.height(10.dp))
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    item.tags.forEach { tag ->
                        Surface(
                            shape = RoundedCornerShape(12.dp),
                            color = Color.White.copy(alpha = 0.05f)
                        ) {
                            Text(
                                text = "#$tag",
                                style = MaterialTheme.typography.labelSmall.copy(
                                    fontSize = 10.sp,
                                    fontWeight = FontWeight.Normal
                                ),
                                color = TextTertiaryDark,
                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}
