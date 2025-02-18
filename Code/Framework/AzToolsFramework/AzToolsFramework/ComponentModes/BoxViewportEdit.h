/*
 * Copyright (c) Contributors to the Open 3D Engine Project.
 * For complete copyright and license terms please see the LICENSE at the root of this distribution.
 *
 * SPDX-License-Identifier: Apache-2.0 OR MIT
 *
 */

#pragma once

#include <AzCore/Component/ComponentBus.h>
#include <AzToolsFramework/ComponentModes/BaseViewportEdit.h>
#include <AzToolsFramework/Manipulators/LinearManipulator.h>

namespace AzToolsFramework
{
    class LinearManipulator;

    /// Wraps 6 linear manipulators, providing a viewport experience for 
    /// modifying the extents of a box
    class BoxViewportEdit : public BaseViewportEdit
    {
    public:
        BoxViewportEdit(bool allowAsymmetricalEditing = false);

        // BaseViewportEdit overrides ...
        void Setup(const AZ::EntityComponentIdPair& entityComponentIdPair) override;
        void Teardown() override;
        void UpdateManipulators() override;
        void ResetValues() override;

    private:
        AZ::EntityComponentIdPair m_entityComponentIdPair;
        using BoxManipulators = AZStd::array<AZStd::shared_ptr<LinearManipulator>, 6>;
        BoxManipulators m_linearManipulators; ///< Manipulators for editing box size.
        bool m_allowAsymmetricalEditing = false; ///< Whether moving individual faces independently is allowed.
    };
} // namespace AzToolsFramework
