// no function at 0x00480080

// ==== FUN_00493440 @ 00493440  (239 bytes) ====

void FUN_00493440(undefined4 param_1,int param_2,byte *param_3)

{
  byte bVar1;
  byte *pbVar2;
  uint uVar3;
  char *pcVar4;
  bool bVar5;
  
  pcVar4 = "AccountId";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_00493470:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_00493475;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_00493470;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_00493475:
  if (uVar3 == 0) {
    FUN_009a8d30(param_2 + 4);
    return;
  }
  pcVar4 = "ConnectionToken";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_004934b4:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_004934b9;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_004934b4;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_004934b9:
  if (uVar3 == 0) {
    FUN_009a9450(param_2 + 0xc,*(undefined4 *)(param_2 + 8));
    return;
  }
  pcVar4 = "ProfileId";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_00493500:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_00493505;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_00493500;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_00493505:
  if (uVar3 == 0) {
    FUN_009a9450(param_2 + 0x2c,*(undefined4 *)(param_2 + 0x28));
    return;
  }
  FUN_009a9ce0("LoginResult",param_3,0);
  return;
}



// ==== FUN_0049de80 @ 0049de80  (88 bytes) ====

undefined4 FUN_0049de80(undefined4 param_1,int param_2)

{
  int iVar1;
  
  iVar1 = param_2 + 4;
  FUN_009ab550("AccountId");
  FUN_009aad80(iVar1);
  FUN_009ab550("ConnectionToken");
  FUN_009ab060(param_2 + 0xc);
  FUN_009ab550("ProfileId");
  FUN_009ab060(param_2 + 0x2c);
  return 1;
}



// no function at 0x004354f0

// ==== FUN_00444fb0 @ 00444fb0  (321 bytes) ====

void FUN_00444fb0(undefined4 param_1,int param_2,byte *param_3)

{
  byte bVar1;
  byte *pbVar2;
  uint uVar3;
  char *pcVar4;
  bool bVar5;
  
  pcVar4 = "AccountName";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_00444fe0:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_00444fe5;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_00444fe0;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_00444fe5:
  if (uVar3 == 0) {
    FUN_009a9450(param_2 + 8,*(undefined4 *)(param_2 + 4));
    return;
  }
  pcVar4 = "AccountPassword";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_00445027:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_0044502c;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_00445027;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_0044502c:
  if (uVar3 == 0) {
    FUN_009a9450(param_2 + 0x10c,*(undefined4 *)(param_2 + 0x108));
    return;
  }
  pcVar4 = "GameServerUrl";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_00445073:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_00445078;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_00445073;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_00445078:
  if (uVar3 == 0) {
    FUN_009a9450(param_2 + 0x210,*(undefined4 *)(param_2 + 0x20c));
    return;
  }
  pcVar4 = "HttpCompression";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_004450c0:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_004450c5;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_004450c0;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_004450c5:
  if (uVar3 == 0) {
    FUN_009a8c90(param_2 + 0x310);
    return;
  }
  FUN_009a9ce0("GameServerConnectionConfig",param_3,0);
  return;
}



// ==== FUN_005e19d0 @ 005e19d0  (5 bytes) ====

undefined1 FUN_005e19d0(void)

{
  return 1;
}



// no function at 0x0060a7a0

// ==== FUN_00615db0 @ 00615db0  (465 bytes) ====

void FUN_00615db0(undefined4 param_1,int param_2,byte *param_3)

{
  byte bVar1;
  byte *pbVar2;
  uint uVar3;
  char *pcVar4;
  bool bVar5;
  
  pcVar4 = "AccountId";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_00615de0:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_00615de5;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_00615de0;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_00615de5:
  if (uVar3 == 0) {
    FUN_009a8d30(param_2 + 4);
    return;
  }
  pcVar4 = "ActivationStatus";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_00615e24:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_00615e29;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_00615e24;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_00615e29:
  if (uVar3 == 0) {
    FUN_009a8d30(param_2 + 8);
    return;
  }
  pcVar4 = "DisplayName";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_00615e68:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_00615e6d;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_00615e68;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_00615e6d:
  if (uVar3 == 0) {
    FUN_009a9450(param_2 + 0x10,*(undefined4 *)(param_2 + 0xc));
    return;
  }
  pcVar4 = "Email";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_00615eb0:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_00615eb5;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_00615eb0;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_00615eb5:
  if (uVar3 == 0) {
    FUN_009a9450(param_2 + 0x114,*(undefined4 *)(param_2 + 0x110));
    return;
  }
  pcVar4 = "Password";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_00615f00:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_00615f05;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_00615f00;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_00615f05:
  if (uVar3 == 0) {
    FUN_009a9450(param_2 + 0x218,*(undefined4 *)(param_2 + 0x214));
    return;
  }
  pcVar4 = "Privileges";
  pbVar2 = param_3;
  do {
    bVar1 = *pbVar2;
    bVar5 = bVar1 < (byte)*pcVar4;
    if (bVar1 != *pcVar4) {
LAB_00615f50:
      uVar3 = -(uint)bVar5 | 1;
      goto LAB_00615f55;
    }
    if (bVar1 == 0) break;
    bVar1 = pbVar2[1];
    bVar5 = bVar1 < (byte)pcVar4[1];
    if (bVar1 != pcVar4[1]) goto LAB_00615f50;
    pbVar2 = pbVar2 + 2;
    pcVar4 = pcVar4 + 2;
  } while (bVar1 != 0);
  uVar3 = 0;
LAB_00615f55:
  if (uVar3 == 0) {
    FUN_009a9440(param_2 + 0x318);
    return;
  }
  FUN_009a9ce0("AccountLite",param_3,0);
  return;
}



// ==== FUN_00626c30 @ 00626c30  (166 bytes) ====

undefined4 FUN_00626c30(undefined4 param_1,int param_2)

{
  int iVar1;
  
  iVar1 = param_2 + 4;
  FUN_009ab550("AccountId");
  FUN_009aad80(iVar1);
  iVar1 = param_2 + 8;
  FUN_009ab550("ActivationStatus");
  FUN_009aad80(iVar1);
  FUN_009ab550("DisplayName");
  FUN_009ab060(param_2 + 0x10);
  FUN_009ab550("Email");
  FUN_009ab060(param_2 + 0x114);
  FUN_009ab550("Password");
  FUN_009ab060(param_2 + 0x218);
  param_2 = param_2 + 0x318;
  FUN_009ab550("Privileges");
  FUN_009ab010(param_2);
  return 1;
}



