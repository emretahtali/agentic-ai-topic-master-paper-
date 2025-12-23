package com.ellitoken.myapplication.presentation.screens.profile.components

import androidx.annotation.DrawableRes
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.material3.Icon
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ellitoken.myapplication.ui.theme.appBlue
import com.ellitoken.myapplication.ui.theme.appFirstGray

@Composable
fun LineInfoWithToggleBar(modifier : Modifier = Modifier, text : String, checked: Boolean,
                          onCheckedChange: (Boolean) -> Unit
                          ,@DrawableRes icon : Int) {
    Row (modifier = modifier, horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically){
        Row(modifier = Modifier, verticalAlignment = Alignment.CenterVertically ) {
            Icon(
                painter = painterResource(id = icon),
                contentDescription = "",
                modifier = Modifier.size(20.dp)
            )

            Spacer(Modifier.width(8.dp))

            Text(
                text = text,
                color = Color.Black,
                fontSize = 14.sp,
                fontWeight = FontWeight.W400
            )

        }
        Switch(
            checked = checked,
            onCheckedChange = onCheckedChange,
            modifier = Modifier
                .scale(0.9f)
                .height(32.dp).padding(end = 8.dp),
            colors = SwitchDefaults.colors(
                checkedThumbColor  = Color.White,
                checkedTrackColor  = appBlue,
                uncheckedThumbColor = Color.White,
                uncheckedTrackColor = appFirstGray
            )
        )
    }
}