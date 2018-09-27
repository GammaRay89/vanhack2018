//
//  SCNKitViewController.swift
//  MenuWise
//
//  Created by Joseph Deeth on 2018-09-23.
//  Copyright © 2018 thomas minshull. All rights reserved.
//

import UIKit
import SceneKit

class SCNKitViewController: UIViewController {
    @IBOutlet weak var scnView: SCNView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        scnView.scene = SCNScene(named: "Golden_Fish_DAE")
        scnView.allowsCameraControl = true
        scnView.autoenablesDefaultLighting = true
        scnView.backgroundColor = UIColor.gray
        
    }

}
