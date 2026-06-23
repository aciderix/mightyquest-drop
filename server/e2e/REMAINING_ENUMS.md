# Remaining flagged enum fields (the ~8%) — value-ambiguous, need per-field enum type

These 91 contracts emit an enum NAME the gate can't safely convert because the
value maps to different integers in different enums (e.g. Type='Ability' is 10 in
EntityType but 1 in {Stat,Ability}). They are ALL UI models / news / tooltips /
event-args — no gameplay-flow contract is here (those are clean). Each is traced
live in server/uncertain.log; close one by recovering its field's static enum type.

| contract | unresolved field=value |
|---|---|
| AbilityLevelAutoAimParam | AutoAimType=Area, TargetType=Hero |
| AbstractFriendNewsData | Type=Ability |
| AttackSelectionCastlePanelNavigationModel | Category=Armor, Type=Ability |
| BattleLogEntry | Type=Ability |
| BossKilledFriendNewsData | Type=Ability |
| BuffTooltipModel | Type=Ability |
| BuildEntitiesAchievement | EntityType=Creature |
| BuildEntityEventArgs | SpecContainerType=Building |
| BuildingTooltipModel | Type=Ability |
| BuyNewTabTooltipModel | Type=Ability |
| CastleAttackedNotification | Type=Ability |
| CastleCell | Type=Ability |
| CastleInventoryAction | Type=Ability |
| CastleInventoryAddedAction | Type=Ability |
| CastleInventoryRemovedAction | Type=Ability |
| CastleObjectiveStatusModel | Category=Armor, Type=Ability |
| CastleObjectiveStatusUpdatedEventArgs | Category=Armor, Type=Ability |
| CastlePopupRewardsTooltipModel | Type=Ability |
| CastlePopupStarsTooltipModel | Type=Ability |
| CastleRatedNotification | Type=Ability |
| ChatInhibitionRule | Type=Ability |
| CompetitionEndedNoRewardsNewsData | Type=Ability |
| ConsumableTooltipModel | Type=Ability |
| CraftingMaterialMineTooltipModel | Type=Ability |
| CraftingMaterialsPackModel | Type=Ability |
| CraftingStampingCounterModel | Type=Ability |
| CreatureTrapTooltipModel | Type=Ability |
| CsvProperty | Type=Ability |
| DecorationTooltipModel | Type=Ability |
| DefendLogEntry | Type=Ability |
| DefendLogEntryModel | Type=Ability |
| DefendLogEventArgs | Type=Ability |
| EquipmentTooltipModel | Type=Ability |
| ErrorMessageModel | Type=Ability |
| ForgeItemCollectModel | Type=Ability |
| ForgeItemSelectionEventArgs | EquipUserInterfaceSoundId=EquipArmorSound |
| ForgeMysteryBoxItemModel | EquipUserInterfaceSoundId=EquipArmorSound |
| ForgeMysteryBoxModel | EquipUserInterfaceSoundId=EquipArmorSound |
| FriendRewardGrantedNewsData | Type=Ability |
| HeroBiographyPanelNavigationModel | Type=Ability |
| HeroCorpseHarvestingTooltipModel | Type=Ability |
| HeroCreationHeroInfo | Type=Ability |
| HeroInventoryItemModel | EquipUserInterfaceSoundId=EquipArmorSound |
| HeroItemEffectTemplate | Type=Ability |
| HeroItemType | EquipUserInterfaceSoundId=EquipArmorSound |
| HeroLevelUpOwnNewsData | Type=Ability |
| HeroTooltipModel | Type=Ability |
| HeroUpgradeTooltipModel | Type=Ability |
| ItemEffect | Type=Ability |
| JobSummary | Type=Ability |
| KillEntitiesAchievement | EntityType=Creature |
| LeagueRankReachedNewsData | Type=Ability |
| LeagueUpdatedNewsData | Type=Ability |
| MagicalPropertyModel | Type=Ability |
| Message | Type=Ability |
| MessageBoxAssignmentActionSpec | Type=Ability |
| MessagePreview | Type=Ability |
| NewsCategorySettings | Type=Ability |
| NewsData | Type=Ability |
| ObjectiveEntryModel | Category=Armor, Type=Ability |
| ObjectivePopupClosedEventArgs | Category=Armor, Type=Ability |
| ObjectiveSummaryEntryModel | Category=Armor, Type=Ability |
| OptionInformation | Category=Armor |
| OptionParameterBaseModel | Type=Ability |
| OptionParameterCheckboxModel | Type=Ability |
| OptionParameterComboboxModel | Type=Ability |
| OptionParameterSliderModel | Type=Ability |
| PackageVersionInfoIdTracking | Type=Ability |
| PopupAssignmentActionSpec | Type=Ability |
| PopupOnTargetAssignmentActionSpec | Type=Ability |
| PopupOptionsModel | Type=Ability |
| ProceduralRoomBuildableSpawnInfo | RoomBuildableType=Cannon |
| RoomObject | EffectName=ChestsOpeningTrigger, SpecContainerType=Building |
| RoomTooltipModel | RoomModelCategory=Corner, Type=Ability |
| SetLastViewedDateCommand | Type=Ability |
| ShopCategoryFilter | Type=Ability |
| ShopCategorySettings | Category=Armor |
| ShopFilter | Type=Ability |
| ShopFilterModel | Type=Ability |
| ShopFilterValueId | Type=Ability |
| ShopProductModel | Type=Ability |
| ShowTooltipEventArgs | Type=Ability |
| SpellTooltipModel | Type=Ability |
| TooltipModel | Type=Ability |
| TotemTooltipModel | Type=Ability |
| TrapTooltipModel | Type=Ability |
| UIGridItemModel | Type=Ability |
| ValidationAttemptNewsData | Type=Ability |
| ViewableItem | Type=Ability |
| VisualAnimatedEntitySettings | BuilderDrag=IT_Drag, BuilderDrop=IT_Drop, CloseDoor=Door_Closing, ClosedDoor=Door_StateClosed, CreateObstacle=CreateObstacle, DamageObstacle=DamageObstacle, DefaultAttachmentBone=Bip01, DestroyObstacle=DestroyObstacle, Harvest=IT_Purchase, LootAction=Action, OpenDoor=Door_Opening, OpenedDoor=Door_StateOpen |
| WorldRankReachedNewsData | Type=Ability |
